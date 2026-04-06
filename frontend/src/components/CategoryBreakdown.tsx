"use client";

import { useEffect, useState } from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";
import { api, CategoryBreakdownItem } from "@/lib/api";

const COLORS = ["#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd", "#ddd6fe", "#ede9fe"];

export default function CategoryBreakdown() {
  const [data, setData] = useState<CategoryBreakdownItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .categoryBreakdown("30d")
      .then(setData)
      .catch(() => setData([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-6 h-80 flex items-center justify-center">
        <p className="text-zinc-500">Loading...</p>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-6 h-80 flex items-center justify-center">
        <p className="text-zinc-500 text-sm">No category data yet.</p>
      </div>
    );
  }

  const chartData = data.map((d) => ({
    name: d.category,
    value: parseFloat(d.volume_usd),
    pct: d.percentage.toFixed(1),
  }));

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-6">
      <h2 className="text-lg font-semibold text-white mb-4">Category Breakdown</h2>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            dataKey="value"
            nameKey="name"
            paddingAngle={2}
          >
            {chartData.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{ background: "#18181b", border: "1px solid #3f3f46", borderRadius: 8 }}
            formatter={(v) => [`$${Number(v).toLocaleString()}`, "Volume"]}
          />
          <Legend
            formatter={(value: string) => <span className="text-zinc-300 text-sm">{value}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
