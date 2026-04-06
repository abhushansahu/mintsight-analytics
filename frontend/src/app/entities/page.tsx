"use client";

import { Suspense } from "react";
import EntityExplorer from "@/components/EntityExplorer";

export default function EntitiesPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-white">Entities</h2>
        <p className="text-sm text-zinc-400">Explore enriched entities and drill into individual profiles.</p>
      </div>

      <Suspense fallback={<div className="text-sm text-zinc-500">Loading…</div>}>
        <EntityExplorer />
      </Suspense>
    </div>
  );
}

