"use client";

import { useEffect, useState } from "react";
import { api, TopMerchant } from "@/lib/api";

export default function TopMerchants() {
  const [merchants, setMerchants] = useState<TopMerchant[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .topMerchants("30d")
      .then(setMerchants)
      .catch(() => setMerchants([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-6">
      <h2 className="text-lg font-semibold text-white mb-4">Top Merchants</h2>
      {loading ? (
        <p className="text-zinc-500">Loading...</p>
      ) : merchants.length === 0 ? (
        <p className="text-zinc-500 text-sm">No merchant data yet.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-zinc-400 border-b border-zinc-800">
                <th className="text-left py-2 pr-4">#</th>
                <th className="text-left py-2 pr-4">Entity</th>
                <th className="text-left py-2 pr-4">Category</th>
                <th className="text-right py-2 pr-4">Volume (USD)</th>
                <th className="text-right py-2">Txns</th>
              </tr>
            </thead>
            <tbody>
              {merchants.map((m, i) => (
                <tr key={m.entity_slug} className="border-b border-zinc-800/50 hover:bg-zinc-800/30">
                  <td className="py-2 pr-4 text-zinc-500">{i + 1}</td>
                  <td className="py-2 pr-4 text-white font-medium">{m.entity_name}</td>
                  <td className="py-2 pr-4">
                    <span className="px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-300 text-xs">
                      {m.category}
                    </span>
                  </td>
                  <td className="py-2 pr-4 text-right text-emerald-400 font-mono">
                    ${parseFloat(m.volume_usd).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                  </td>
                  <td className="py-2 text-right text-zinc-300 font-mono">
                    {m.transaction_count.toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
