"use client";

import { useEffect, useState } from "react";
import { api, EntityInfo } from "@/lib/api";
import { useUrlSelectors } from "@/lib/useUrlSelectors";

export default function EntityExplorer() {
  const [entities, setEntities] = useState<EntityInfo[]>([]);
  const { selectors, replace } = useUrlSelectors();
  const search = selectors.search ?? "";
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const params: Record<string, string> = { limit: "50" };
    if (search) params.search = search;
    const timer = setTimeout(() => {
      api
        .entities(params)
        .then(setEntities)
        .catch(() => setEntities([]))
        .finally(() => setLoading(false));
    }, 300);
    return () => clearTimeout(timer);
  }, [search]);

  const CATEGORY_COLORS: Record<string, string> = {
    exchange: "bg-cyan-500/20 text-cyan-400",
    defi: "bg-purple-500/20 text-purple-400",
    dex: "bg-purple-500/20 text-purple-400",
    retail: "bg-emerald-500/20 text-emerald-400",
    infrastructure: "bg-blue-500/20 text-blue-400",
    payment_processor: "bg-amber-500/20 text-amber-400",
    wallet: "bg-zinc-700/50 text-zinc-400",
  };

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-white">Entity Explorer</h2>
        <input
          type="text"
          placeholder="Search entities..."
          value={search}
          onChange={(e) => {
            replace({ search: e.target.value });
            setLoading(true);
          }}
          className="px-3 py-1.5 rounded-lg bg-zinc-800 border border-zinc-700 text-sm text-white placeholder:text-zinc-500 focus:outline-none focus:border-indigo-500 w-60"
        />
      </div>
      {loading ? (
        <p className="text-zinc-500">Loading...</p>
      ) : entities.length === 0 ? (
        <p className="text-zinc-500 text-sm">No entities found. Seed the entity database first.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-[500px] overflow-y-auto pr-2">
          {entities.map((e) => (
            <div key={e.slug} className="p-3 rounded-lg bg-zinc-800/40 hover:bg-zinc-800/60 transition">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-white font-medium text-sm">{e.name}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${CATEGORY_COLORS[e.category] || "bg-zinc-700/50 text-zinc-400"}`}>
                  {e.category}
                </span>
              </div>
              {e.description && (
                <p className="text-xs text-zinc-500 line-clamp-2">{e.description}</p>
              )}
              {e.website && (
                <a href={e.website} target="_blank" rel="noopener noreferrer" className="text-xs text-indigo-400 hover:underline mt-1 block">
                  {e.website.replace(/^https?:\/\//, "")}
                </a>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
