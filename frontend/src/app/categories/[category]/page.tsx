"use client";

import Link from "next/link";
import { useParams } from "next/navigation";

export default function CategoryDetailPage() {
  const params = useParams<{ category?: string }>();
  const category = typeof params?.category === "string" ? params.category : "unknown";

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <Link href="/categories" className="text-sm text-zinc-400 hover:text-zinc-200">
          ← Back to Categories
        </Link>
      </div>

      <div>
        <h2 className="text-xl font-semibold text-white">Category</h2>
        <p className="text-sm text-zinc-400">{category}</p>
      </div>

      <div className="rounded-xl border border-zinc-800 bg-zinc-950/40 p-4">
        <p className="text-sm text-zinc-300">
          Placeholder for category drilldown. Next step is to reuse the existing widgets but filtered to this category.
        </p>
      </div>
    </div>
  );
}

