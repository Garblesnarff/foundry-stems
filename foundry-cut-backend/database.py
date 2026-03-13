from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

import aiosqlite

from config import DB_PATH, DEFAULT_MODEL, DEFAULT_NUM_THREADS, DEFAULT_OUTPUT_FORMAT, DEFAULT_SAMPLE_RATE, OUTPUT_DIR


CREATE_JOBS_TABLE = """
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'queued',
    input_filename TEXT NOT NULL,
    input_path TEXT NOT NULL,
    output_dir TEXT,
    model TEXT NOT NULL DEFAULT 'htdemucs',
    stems TEXT NOT NULL DEFAULT '["vocals","drums","bass","other"]',
    output_format TEXT NOT NULL DEFAULT 'wav',
    sample_rate INTEGER NOT NULL DEFAULT 44100,
    input_duration_seconds REAL,
    input_sample_rate INTEGER,
    input_channels INTEGER,
    input_format TEXT,
    progress_percent REAL DEFAULT 0,
    progress_stage TEXT,
    processing_time_seconds REAL,
    error_message TEXT,
    created_at TEXT NOT NULL,
    started_at TEXT,
    completed_at TEXT
);
"""

CREATE_STEMS_TABLE = """
CREATE TABLE IF NOT EXISTS stems (
    id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL,
    name TEXT NOT NULL,
    output_path TEXT NOT NULL,
    format TEXT NOT NULL,
    duration_seconds REAL NOT NULL,
    sample_rate INTEGER NOT NULL,
    file_size_bytes INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);
"""

CREATE_SETTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


def now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        await db.execute(CREATE_JOBS_TABLE)
        await db.execute(CREATE_STEMS_TABLE)
        await db.execute(CREATE_SETTINGS_TABLE)
        await db.commit()
    await seed_settings()
    await mark_interrupted_jobs_failed()


async def seed_settings() -> None:
    defaults = {
        "model": DEFAULT_MODEL,
        "output_format": DEFAULT_OUTPUT_FORMAT,
        "sample_rate": str(DEFAULT_SAMPLE_RATE),
        "num_threads": str(DEFAULT_NUM_THREADS),
        "output_directory": str(OUTPUT_DIR),
        "auto_cleanup_days": "30",
    }
    async with aiosqlite.connect(DB_PATH) as db:
        for k, v in defaults.items():
            await db.execute("INSERT OR IGNORE INTO settings(key, value) VALUES(?, ?)", (k, v))
        await db.commit()


async def mark_interrupted_jobs_failed() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """UPDATE jobs SET status='failed', error_message='Interrupted by shutdown/crash', completed_at=?
            WHERE status='processing'""",
            (now_iso(),),
        )
        await db.commit()


async def fetch_settings() -> dict[str, Any]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute("SELECT key, value FROM settings")).fetchall()
    data = {r["key"]: r["value"] for r in rows}
    return {
        "model": data.get("model", DEFAULT_MODEL),
        "output_format": data.get("output_format", DEFAULT_OUTPUT_FORMAT),
        "sample_rate": int(data.get("sample_rate", DEFAULT_SAMPLE_RATE)),
        "num_threads": int(data.get("num_threads", DEFAULT_NUM_THREADS)),
        "output_directory": data.get("output_directory", str(OUTPUT_DIR)),
        "auto_cleanup_days": int(data.get("auto_cleanup_days", 30)),
    }


async def update_settings(payload: dict[str, Any]) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        for key, value in payload.items():
            await db.execute("INSERT INTO settings(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, str(value)))
        await db.commit()


async def create_job(data: dict[str, Any]) -> None:
    keys = ",".join(data.keys())
    placeholders = ",".join(["?"] * len(data))
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"INSERT INTO jobs ({keys}) VALUES ({placeholders})", tuple(data.values()))
        await db.commit()


async def update_job(job_id: str, data: dict[str, Any]) -> None:
    if not data:
        return
    clause = ", ".join([f"{k}=?" for k in data.keys()])
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"UPDATE jobs SET {clause} WHERE id=?", (*data.values(), job_id))
        await db.commit()


async def get_job(job_id: str) -> dict[str, Any] | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        job = await (await db.execute("SELECT * FROM jobs WHERE id=?", (job_id,))).fetchone()
        if not job:
            return None
        job_d = dict(job)
        job_d["stems"] = json.loads(job_d["stems"])
        stems = await (await db.execute("SELECT * FROM stems WHERE job_id=?", (job_id,))).fetchall()
        job_d["stem_files"] = [dict(s) for s in stems]
        return job_d


async def list_jobs(status: str | None = None) -> list[dict[str, Any]]:
    query = "SELECT * FROM jobs"
    params: tuple[Any, ...] = ()
    if status:
        query += " WHERE status=?"
        params = (status,)
    query += " ORDER BY created_at ASC"
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute(query, params)).fetchall()
    jobs = []
    for row in rows:
        d = dict(row)
        d["stems"] = json.loads(d["stems"])
        jobs.append(d)
    return jobs


async def add_stem(data: dict[str, Any]) -> None:
    keys = ",".join(data.keys())
    placeholders = ",".join(["?"] * len(data))
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"INSERT INTO stems ({keys}) VALUES ({placeholders})", tuple(data.values()))
        await db.commit()


async def delete_job(job_id: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM jobs WHERE id=?", (job_id,))
        await db.commit()


async def delete_history() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM stems")
        await db.execute("DELETE FROM jobs")
        await db.commit()


async def history(search: str = "", sort: str = "newest", limit: int = 50, offset: int = 0) -> tuple[list[dict[str, Any]], int]:
    sort_clause = {
        "newest": "created_at DESC",
        "oldest": "created_at ASC",
        "longest": "input_duration_seconds DESC",
        "shortest": "input_duration_seconds ASC",
    }.get(sort, "created_at DESC")
    where = "WHERE status='completed'"
    params: list[Any] = []
    if search:
        where += " AND input_filename LIKE ?"
        params.append(f"%{search}%")
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        total = (await (await db.execute(f"SELECT COUNT(*) as c FROM jobs {where}", tuple(params))).fetchone())["c"]
        rows = await (
            await db.execute(
                f"SELECT * FROM jobs {where} ORDER BY {sort_clause} LIMIT ? OFFSET ?",
                tuple(params + [limit, offset]),
            )
        ).fetchall()
        jobs = []
        for row in rows:
            d = dict(row)
            d["stems"] = json.loads(d["stems"])
            srows = await (await db.execute("SELECT * FROM stems WHERE job_id=?", (d["id"],))).fetchall()
            d["stem_files"] = [dict(s) for s in srows]
            jobs.append(d)
    return jobs, total


async def stats() -> dict[str, Any]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        row = await (
            await db.execute(
                """SELECT COUNT(*) jobs_completed,
                COALESCE(SUM(input_duration_seconds),0) total_input_seconds,
                COALESCE(SUM(processing_time_seconds),0) total_processing_seconds
                FROM jobs WHERE status='completed'"""
            )
        ).fetchone()
    ratio = (row["total_processing_seconds"] / row["total_input_seconds"]) if row["total_input_seconds"] else 0
    payload = {
        "jobs_completed": row["jobs_completed"],
        "total_input_seconds": row["total_input_seconds"],
        "total_processing_seconds": row["total_processing_seconds"],
        "avg_speed_ratio": ratio,
    }
    return {"session": payload, "lifetime": payload}
