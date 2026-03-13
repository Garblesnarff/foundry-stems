export function HistoryFilters({ search, setSearch, sort, setSort }: { search: string; setSearch: (s: string)=>void; sort: string; setSort: (s:string)=>void }) {
  return <div className="flex gap-3"><input className="input-field" placeholder="Search forge history" value={search} onChange={(e)=>setSearch(e.target.value)} /><select className="select-field" value={sort} onChange={(e)=>setSort(e.target.value)}><option value="newest">Newest</option><option value="oldest">Oldest</option><option value="longest">Longest</option><option value="shortest">Shortest</option></select></div>
}
