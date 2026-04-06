"use client";

import Link from "next/link";
import { Suspense, useEffect, useMemo, useState } from "react";
import { api, CommerceFlowItem } from "@/lib/api";
import { useUrlSelectors } from "@/lib/useUrlSelectors";

function formatUsd(v: string) {
  const n = Number(v);
  if (!Number.isFinite(n)) return v;
  return n.toLocaleString(undefined, { maximumFractionDigits: 0 });
}

function FlowsInner() {
  const { selectors, replace, PERIODS, INTERVALS } = useUrlSelectors({ period: "30d", interval: "1d" });
  const [data, setData] = useState<CommerceFlowItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api
      .commerceFlow(selectors.period)
      .then(setData)
      .catch(() => setData([]))
      .finally(() => setLoading(false));
  }, [selectors.period]);

  const cards = useMemo(() => {
    return data
      .slice()
      .sort((a, b) => Number(b.volume_usd) - Number(a.volume_usd))
      .map((d) => ({
        commerceType: d.commerce_type || "unknown",
        volumeUsd: d.volume_usd,
        txns: d.transaction_count,
        pct: d.percentage,
      }));
  }, [data]);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-white">Flows</h2>
        <p className="text-sm text-zinc-400">Start from a commerce type, then drill down into transactions and top entities.</p>
      </div>

      <div className="rounded-xl border border-zinc-800 bg-zinc-950/40 p-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <label className="space-y-1">
            <div className="text-xs text-zinc-500">Period</div>
            <select
              value={selectors.period}
              onChange={(e) => replace({ period: e.target.value as typeof selectors.period })}
              className="w-full rounded-lg bg-zinc-900 border border-zinc-800 px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
            >
              {PERIODS.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </label>
          <label className="space-y-1">
            <div className="text-xs text-zinc-500">Interval (preserved into drilldowns)</div>
            <select
              value={selectors.interval}
              onChange={(e) => replace({ interval: e.target.value as typeof selectors.interval })}
              className="w-full rounded-lg bg-zinc-900 border border-zinc-800 px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
            >
              {INTERVALS.map((i) => (
                <option key={i} value={i}>
                  {i}
                </option>
              ))}
            </select>
          </label>
        </div>
      </div>

      {loading ? (
        <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-6 h-48 flex items-center justify-center">
          <p className="text-zinc-500">Loading...</p>
        </div>
      ) : cards.length === 0 ? (
        <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-6 h-48 flex items-center justify-center">
          <p className="text-zinc-500 text-sm">No flow data yet.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {cards.map((c) => {
            const href = `/flows/${encodeURIComponent(c.commerceType)}?period=${selectors.period}&interval=${selectors.interval}`;
            return (
              <Link
                key={c.commerceType}
                href={href}
                className="rounded-xl border border-zinc-800 bg-zinc-950/40 p-4 hover:bg-zinc-900/40 transition-colors"
              >
                <div className="flex items-center justify-between gap-3">
                  <div className="min-w-0">
                    <div className="text-sm text-zinc-400">Commerce type</div>
                    <div className="text-lg font-semibold text-white truncate">{c.commerceType}</div>
                  </div>
                  <div className="text-right shrink-0">
                    <div className="text-sm text-zinc-200">{Number.isFinite(Number(c.pct)) ? `${c.pct.toFixed(1)}%` : "-"}</div>
                    <div className="text-xs text-zinc-500">share</div>
                  </div>
                </div>

                <div className="mt-4 grid grid-cols-2 gap-3">
                  <div className="rounded-lg bg-zinc-900/50 border border-zinc-800 p-3">
                    <div className="text-xs text-zinc-500">Volume (USD)</div>
                    <div className="text-sm font-mono text-white">${formatUsd(c.volumeUsd)}</div>
                  </div>
                  <div className="rounded-lg bg-zinc-900/50 border border-zinc-800 p-3">
                    <div className="text-xs text-zinc-500">Txns</div>
                    <div className="text-sm font-mono text-white">{Number(c.txns).toLocaleString()}</div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default function FlowsPage() {
  return (
    <Suspense fallback={<div className="text-sm text-zinc-500">Loading…</div>}>
      <FlowsInner />
    </Suspense>
  );
}

