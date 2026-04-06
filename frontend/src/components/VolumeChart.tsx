"use client";

import { useEffect, useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { api, VolumePoint } from "@/lib/api";

export default function VolumeChart() {
  const [data, setData] = useState<VolumePoint[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .volume("1d", "30d")
      .then((res) => setData(res.data))
      .catch(() => setData([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-6 h-80 flex items-center justify-center">
        <p className="text-zinc-500">Loading volume data...</p>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-6 h-80 flex items-center justify-center">
        <p className="text-zinc-500">No volume data yet. Ingest transactions to see charts.</p>
      </div>
    );
  }

  const formatted = data.map((d) => ({
    ...d,
    date: new Date(d.timestamp).toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    vol: parseFloat(d.volume_usd),
  }));

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-6">
      <h2 className="text-lg font-semibold text-white mb-4">Volume (USD) — Last 30 Days</h2>
      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={formatted}>
          <defs>
            <linearGradient id="volGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
          <XAxis dataKey="date" stroke="#71717a" fontSize={12} />
          <YAxis stroke="#71717a" fontSize={12} tickFormatter={(v: number) => `$${(v / 1000).toFixed(0)}k`} />
          <Tooltip
            contentStyle={{ background: "#18181b", border: "1px solid #3f3f46", borderRadius: 8 }}
            labelStyle={{ color: "#a1a1aa" }}
            formatter={(v) => [`$${Number(v).toLocaleString()}`, "Volume"]}
          />
          <Area type="monotone" dataKey="vol" stroke="#6366f1" fill="url(#volGrad)" strokeWidth={2} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
