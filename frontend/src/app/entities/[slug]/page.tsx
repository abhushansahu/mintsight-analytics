"use client";

import { useParams } from "next/navigation";
import Link from "next/link";

export default function EntityDetailPage() {
  const params = useParams<{ slug?: string }>();
  const slug = typeof params?.slug === "string" ? params.slug : "unknown";

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <Link href="/entities" className="text-sm text-zinc-400 hover:text-zinc-200">
          ← Back to Entities
        </Link>
      </div>

      <div>
        <h2 className="text-xl font-semibold text-white">Entity</h2>
        <p className="text-sm text-zinc-400">{slug}</p>
      </div>

      <div className="rounded-xl border border-zinc-800 bg-zinc-950/40 p-4">
        <p className="text-sm text-zinc-300">
          Placeholder for entity drilldown. This route is wired for shareable URLs; next step is to connect it to
          enrichment/entity APIs and reuse any existing widgets.
        </p>
      </div>
    </div>
  );
}

