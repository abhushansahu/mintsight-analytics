const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return res.json();
}

export interface OverviewStats {
  total_transactions: number;
  enriched_transactions: number;
  total_entities: number;
  total_volume_usd: number;
}

export interface EnrichedTransaction {
  id: number;
  signature: string;
  block_time: string;
  source_wallet: string;
  destination_wallet: string;
  mint: string;
  amount: string;
  token_symbol: string | null;
  usd_amount: string | null;
  source_entity: string | null;
  dest_entity: string | null;
  source_category: string | null;
  dest_category: string | null;
  commerce_type: string;
}

export interface EntityInfo {
  id: number;
  name: string;
  slug: string;
  category: string;
  subcategory: string | null;
  website: string | null;
  description: string | null;
}

export interface EntityWithStats extends EntityInfo {
  total_volume_usd: string | null;
  transaction_count: number;
  label_count: number;
}

export interface TopMerchant {
  entity_slug: string;
  entity_name: string;
  category: string;
  volume_usd: string;
  transaction_count: number;
}

export interface CommerceFlowItem {
  commerce_type: string;
  volume_usd: string;
  transaction_count: number;
  percentage: number;
}

export interface CategoryBreakdownItem {
  category: string;
  volume_usd: string;
  transaction_count: number;
  percentage: number;
}

export interface VolumePoint {
  timestamp: string;
  volume_usd: string;
  transaction_count: number;
}

export const api = {
  overview: () => fetchAPI<OverviewStats>("/api/analytics/overview"),

  transactions: (params?: Record<string, string>) => {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return fetchAPI<EnrichedTransaction[]>(`/api/transactions${qs}`);
  },

  entities: (params?: Record<string, string>) => {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return fetchAPI<EntityInfo[]>(`/api/entities${qs}`);
  },

  entity: (slug: string) => fetchAPI<EntityWithStats>(`/api/entities/${slug}`),

  topMerchants: (period = "30d") =>
    fetchAPI<TopMerchant[]>(`/api/analytics/top-merchants?period=${period}`),

  commerceFlow: (period = "30d") =>
    fetchAPI<CommerceFlowItem[]>(`/api/analytics/commerce-flow?period=${period}`),

  categoryBreakdown: (period = "30d") =>
    fetchAPI<CategoryBreakdownItem[]>(`/api/analytics/category-breakdown?period=${period}`),

  volume: (interval = "1d", period = "30d") =>
    fetchAPI<{ data: VolumePoint[] }>(
      `/api/analytics/volume?interval=${interval}&period=${period}`
    ),
};
