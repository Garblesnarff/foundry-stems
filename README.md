# Foundry Cut Scaffold

This repository contains a full local-first scaffold for **Foundry Cut**:
- `foundry-cut-backend/` (FastAPI + Demucs orchestration)
- `foundry-cut-frontend/` (React 19 + Vite + Tailwind)
- `foundry-cut-frontend/src-tauri/` (Tauri 2 shell for macOS packaging)

## Apple App Store readiness (scaffold status)

This pass includes baseline App Store preparation artifacts:
- Tauri bundle metadata configured for macOS app packaging.
- Hardened Runtime enabled in `tauri.conf.json`.
- App Sandbox entitlements added (`entitlements.plist`) for user-selected file access and client networking.
- Rust `build.rs` added for proper tauri-build integration.

## Final pre-submission checklist

Before App Store submission, update and verify:
1. `providerShortName` and `signingIdentity` values in `src-tauri/tauri.conf.json`.
2. Team ID, certificates, notarization pipeline, and CI signing setup.
3. Real app icons, privacy strings, and App Store Connect metadata.
4. Runtime QA on clean Apple Silicon hosts (M1–M4) including long-audio memory behavior.
5. Full frontend/backend integration tests once dependency fetching is available.

