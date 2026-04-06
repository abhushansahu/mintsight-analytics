"use client";

interface StatCardProps {
  label: string;
  value: string | number;
  icon: React.ReactNode;
}

export default function StatCard({ label, value, icon }: StatCardProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-5 backdrop-blur">
      <div className="flex items-center gap-3 text-zinc-400 mb-2">
        {icon}
        <span className="text-sm font-medium uppercase tracking-wide">{label}</span>
      </div>
      <p className="text-2xl font-bold text-white">{typeof value === "number" ? value.toLocaleString() : value}</p>
    </div>
  );
}
