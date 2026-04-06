"use client";

import { useEffect, useState } from "react";
import { Suspense } from "react";
import { Activity, Database, Store, DollarSign } from "lucide-react";
import StatCard from "@/components/StatCard";
import VolumeChart from "@/components/VolumeChart";
import TopMerchants from "@/components/TopMerchants";
import CategoryBreakdown from "@/components/CategoryBreakdown";
import TransactionFeed from "@/components/TransactionFeed";
import EntityExplorer from "@/components/EntityExplorer";
import { api, OverviewStats } from "@/lib/api";

export default function Home() {
  const [stats, setStats] = useState<OverviewStats | null>(null);

  useEffect(() => {
    api.overview().then(setStats).catch(() => setStats(null));
  }, []);

  return (
    <div className="space-y-6">
      {/* Stat cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Transactions"
          value={stats?.total_transactions ?? "—"}
          icon={<Activity size={18} />}
        />
        <StatCard
          label="Enriched"
          value={stats?.enriched_transactions ?? "—"}
          icon={<Database size={18} />}
        />
        <StatCard
          label="Entities"
          value={stats?.total_entities ?? "—"}
          icon={<Store size={18} />}
        />
        <StatCard
          label="Total Volume"
          value={stats ? `$${stats.total_volume_usd.toLocaleString(undefined, { maximumFractionDigits: 0 })}` : "—"}
          icon={<DollarSign size={18} />}
        />
      </div>

      {/* Volume chart */}
      <VolumeChart />

      {/* Two-column: merchants + category */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TopMerchants />
        <CategoryBreakdown />
      </div>

      {/* Transaction feed */}
      <TransactionFeed />

      {/* Entity explorer */}
      <Suspense fallback={<div className="text-sm text-zinc-500">Loading…</div>}>
        <EntityExplorer />
      </Suspense>
    </div>
  );
}
