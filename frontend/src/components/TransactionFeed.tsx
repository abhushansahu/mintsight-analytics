"use client";

import { useEffect, useState } from "react";
import { api, EnrichedTransaction } from "@/lib/api";

function truncateAddr(addr: string) {
  return addr.length > 8 ? `${addr.slice(0, 4)}...${addr.slice(-4)}` : addr;
}

const COMMERCE_COLORS: Record<string, string> = {
  b2b: "bg-blue-500/20 text-blue-400",
  b2c: "bg-emerald-500/20 text-emerald-400",
  c2c: "bg-amber-500/20 text-amber-400",
  protocol: "bg-purple-500/20 text-purple-400",
  exchange: "bg-cyan-500/20 text-cyan-400",
  unknown: "bg-zinc-700/50 text-zinc-400",
};

export default function TransactionFeed() {
  const [txs, setTxs] = useState<EnrichedTransaction[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .transactions({ limit: "25" })
      .then(setTxs)
      .catch(() => setTxs([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-6">
      <h2 className="text-lg font-semibold text-white mb-4">Recent Transactions</h2>
      {loading ? (
        <p className="text-zinc-500">Loading...</p>
      ) : txs.length === 0 ? (
        <p className="text-zinc-500 text-sm">No transactions yet. Send a webhook to ingest data.</p>
      ) : (
        <div className="space-y-2 max-h-[500px] overflow-y-auto pr-2">
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
                  {tx.source_entity && (
                    <span className="text-xs text-indigo-400">({tx.source_entity})</span>
                  )}
                  {tx.dest_entity && (
                    <span className="text-xs text-indigo-400">({tx.dest_entity})</span>
                  )}
                </div>
                <div className="text-xs text-zinc-500 mt-1">
                  {new Date(tx.block_time).toLocaleString()}
                </div>
              </div>
              <div className="text-right shrink-0">
                <div className="text-sm font-mono text-white">
                  {tx.usd_amount ? `$${parseFloat(tx.usd_amount).toLocaleString()}` : `${parseFloat(tx.amount).toLocaleString()} ${tx.token_symbol || "?"}`}
                </div>
                <span className={`text-xs px-2 py-0.5 rounded-full ${COMMERCE_COLORS[tx.commerce_type] || COMMERCE_COLORS.unknown}`}>
                  {tx.commerce_type}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
