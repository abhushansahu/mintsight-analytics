"use client";

import CategoryBreakdown from "@/components/CategoryBreakdown";

export default function CategoriesPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-white">Categories</h2>
        <p className="text-sm text-zinc-400">Browse transaction categories and drill into a category view.</p>
      </div>

      <CategoryBreakdown />

      <div className="rounded-xl border border-zinc-800 bg-zinc-950/40 p-4">
        <p className="text-sm text-zinc-300">
          Placeholder for a category index/list and navigation into <code className="text-zinc-200">/categories/[category]</code>.
        </p>
      </div>
    </div>
  );
}

