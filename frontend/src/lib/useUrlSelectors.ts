import { useCallback, useMemo } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

export type Period = "24h" | "7d" | "30d" | "90d" | "180d" | "1y";
export type Interval = "1h" | "4h" | "1d" | "7d";

export type UrlSelectors = {
  period: Period;
  interval: Interval;
  commerceType?: string;
  category?: string;
  entity?: string;
  mint?: string;
  search?: string;
};

export type UrlSelectorDefaults = Partial<Pick<UrlSelectors, "period" | "interval">>;

const PERIODS: readonly Period[] = ["24h", "7d", "30d", "90d", "180d", "1y"] as const;
const INTERVALS: readonly Interval[] = ["1h", "4h", "1d", "7d"] as const;

function asEnum<T extends string>(v: string | null, allowed: readonly T[]): T | undefined {
  if (!v) return undefined;
  return (allowed as readonly string[]).includes(v) ? (v as T) : undefined;
}

function asNonEmpty(v: string | null): string | undefined {
  const trimmed = (v ?? "").trim();
  return trimmed ? trimmed : undefined;
}

export function useUrlSelectors(defaults: UrlSelectorDefaults = {}) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const selectors = useMemo<UrlSelectors>(() => {
    const period = asEnum(searchParams.get("period"), PERIODS) ?? defaults.period ?? "30d";
    const interval = asEnum(searchParams.get("interval"), INTERVALS) ?? defaults.interval ?? "1d";
    return {
      period,
      interval,
      commerceType: asNonEmpty(searchParams.get("commerceType")),
      category: asNonEmpty(searchParams.get("category")),
      entity: asNonEmpty(searchParams.get("entity")),
      mint: asNonEmpty(searchParams.get("mint")),
      search: asNonEmpty(searchParams.get("search")),
    };
  }, [searchParams, defaults.interval, defaults.period]);

  const replace = useCallback(
    (next: Partial<UrlSelectors>) => {
      const sp = new URLSearchParams(searchParams.toString());
      for (const [k, v] of Object.entries(next)) {
        if (v === undefined || v === null || String(v).trim() === "") sp.delete(k);
        else sp.set(k, String(v));
      }
      const qs = sp.toString();
      router.replace(qs ? `${pathname}?${qs}` : pathname, { scroll: false });
    },
    [pathname, router, searchParams]
  );

  return { selectors, replace, PERIODS, INTERVALS } as const;
}

