"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useUrlSelectors } from "@/lib/useUrlSelectors";
import { Suspense } from "react";
import { api, EnrichedTransaction } from "@/lib/api";
import { useEffect, useMemo, useState } from "react";

function truncateAddr(addr: string) {
  return addr.length > 8 ? `${addr.slice(0, 4)}...${addr.slice(-4)}` : addr;
}

function fromForPeriod(period: string) {
  const now = Date.now();
  const ms =
    period === "24h"
      ? 24 * 60 * 60 * 1000
      : period === "7d"
        ? 7 * 24 * 60 * 60 * 1000
        : period === "30d"
          ? 30 * 24 * 60 * 60 * 1000
          : period === "90d"
            ? 90 * 24 * 60 * 60 * 1000
            : period === "180d"
              ? 180 * 24 * 60 * 60 * 1000
              : period === "1y"
                ? 365 * 24 * 60 * 60 * 1000
                : 30 * 24 * 60 * 60 * 1000;
  return new Date(now - ms).toISOString();
}

function formatUsd(v: string | null) {
  const n = v ? Number(v) : NaN;
  if (!Number.isFinite(n)) return null;
  return n.toLocaleString(undefined, { maximumFractionDigits: 0 });
}

function FlowCommerceTypeInner() {
  const params = useParams<{ commerceType?: string }>();
  const commerceType = typeof params?.commerceType === "string" ? params.commerceType : "unknown";
  const { selectors, replace, PERIODS, INTERVALS } = useUrlSelectors({ period: "30d", interval: "1d" });
  const [txs, setTxs] = useState<EnrichedTransaction[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api
      .transactions({
        commerce_type: commerceType,
        from: fromForPeriod(selectors.period),
        to: new Date().toISOString(),
        limit: "200",
      })
      .then(setTxs)
      .catch(() => setTxs([]))
      .finally(() => setLoading(false));
  }, [commerceType, selectors.period]);

  const topEntities = useMemo(() => {
    const byName = new Map<string, { name: string; txns: number; volumeUsd: number }>();
    for (const tx of txs) {
      const name = tx.dest_entity || tx.source_entity;
      if (!name) continue;
      const vol = tx.usd_amount ? Number(tx.usd_amount) : 0;
      const cur = byName.get(name) ?? { name, txns: 0, volumeUsd: 0 };
      cur.txns += 1;
      cur.volumeUsd += Number.isFinite(vol) ? vol : 0;
      byName.set(name, cur);
    }
    return [...byName.values()].sort((a, b) => b.volumeUsd - a.volumeUsd).slice(0, 10);
  }, [txs]);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <Link
          href={`/flows?period=${selectors.period}&interval=${selectors.interval}`}
          className="text-sm text-zinc-400 hover:text-zinc-200"
        >
          ← Back to Flows
        </Link>
      </div>

      <div>
        <h2 className="text-xl font-semibold text-white">Flow drilldown</h2>
        <p className="text-sm text-zinc-400">
          commerceType: {commerceType} · period: {selectors.period} · interval: {selectors.interval}
        </p>
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
            <div className="text-xs text-zinc-500">Interval</div>
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

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 rounded-xl border border-zinc-800 bg-zinc-900/60 p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Transactions</h3>
          {loading ? (
            <p className="text-zinc-500">Loading...</p>
          ) : txs.length === 0 ? (
            <p className="text-zinc-500 text-sm">No transactions found for this commerce type in the selected period.</p>
          ) : (
            <div className="space-y-2 max-h-[520px] overflow-y-auto pr-2">
              {txs.map((tx) => (
                <div
                  key={`${tx.signature}-${tx.source_wallet}-${tx.destination_wallet}`}
                  className="flex items-center gap-3 p-3 rounded-lg bg-zinc-800/40 hover:bg-zinc-800/60 transition"
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 text-sm">
                      <span className="text-zinc-300 font-mono">{truncateAddr(tx.source_wallet)}</span>
                      <span className="text-zinc-600">&rarr;</span>
                      <span className="text-zinc-300 font-mono">{truncateAddr(tx.destination_wallet)}</span>
                    </div>
                    <div className="text-xs text-zinc-500 mt-1">{new Date(tx.block_time).toLocaleString()}</div>
                    {(tx.source_entity || tx.dest_entity) && (
                      <div className="text-xs text-indigo-400 mt-1 truncate">
                        {tx.source_entity ? `from ${tx.source_entity}` : null}
                        {tx.source_entity && tx.dest_entity ? " · " : null}
                        {tx.dest_entity ? `to ${tx.dest_entity}` : null}
                      </div>
                    )}
                  </div>
                  <div className="text-right shrink-0">
                    <div className="text-sm font-mono text-white">
                      {tx.usd_amount
                        ? `$${formatUsd(tx.usd_amount)}`
                        : `${parseFloat(tx.amount).toLocaleString()} ${tx.token_symbol || "?"}`}
                    </div>
                    <div className="text-xs text-zinc-500">{tx.mint}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Top entities</h3>
          {loading ? (
            <p className="text-zinc-500">Loading...</p>
          ) : topEntities.length === 0 ? (
            <p className="text-zinc-500 text-sm">No enriched entities found in this slice.</p>
          ) : (
            <div className="space-y-2">
              {topEntities.map((e) => (
                <div key={e.name} className="rounded-lg border border-zinc-800 bg-zinc-950/40 p-3">
                  <div className="text-sm text-white truncate">{e.name}</div>
                  <div className="mt-1 flex items-center justify-between text-xs text-zinc-500">
                    <span>{e.txns.toLocaleString()} txns</span>
                    <span>{e.volumeUsd ? `$${e.volumeUsd.toLocaleString(undefined, { maximumFractionDigits: 0 })}` : "-"}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function FlowCommerceTypePage() {
  return (
    <Suspense fallback={<div className="text-sm text-zinc-500">Loading…</div>}>
      <FlowCommerceTypeInner />
    </Suspense>
  );
}

