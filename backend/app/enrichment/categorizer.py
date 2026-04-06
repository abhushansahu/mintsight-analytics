"""Transaction categorizer — classifies commerce type based on entity labels."""

from __future__ import annotations

from app.enrichment.labeler import LabelMatch

BUSINESS_CATEGORIES = {"retail", "saas", "infrastructure", "marketplace", "payment_processor", "logistics"}
INDIVIDUAL_CATEGORIES = {"individual", "wallet"}
PROTOCOL_CATEGORIES = {"defi", "dex", "lending", "bridge", "staking", "oracle"}
EXCHANGE_CATEGORIES = {"exchange", "cex"}


def classify_commerce_type(
    source_label: LabelMatch | None,
    dest_label: LabelMatch | None,
) -> str:
    """Determine the commerce type of a transaction based on source/dest entity labels.

    Categories: b2b, b2c, c2c, protocol, exchange, unknown
    """
    src_cat = source_label.category if source_label else None
    dst_cat = dest_label.category if dest_label else None

    if src_cat in PROTOCOL_CATEGORIES or dst_cat in PROTOCOL_CATEGORIES:
        return "protocol"

    if src_cat in EXCHANGE_CATEGORIES or dst_cat in EXCHANGE_CATEGORIES:
        return "exchange"

    src_is_biz = src_cat in BUSINESS_CATEGORIES
    dst_is_biz = dst_cat in BUSINESS_CATEGORIES

    if src_is_biz and dst_is_biz:
        return "b2b"

    if src_is_biz and not dst_is_biz:
        return "b2c"

    if not src_is_biz and dst_is_biz:
        return "b2c"

    if src_cat in INDIVIDUAL_CATEGORIES and dst_cat in INDIVIDUAL_CATEGORIES:
        return "c2c"

    return "unknown"


WELL_KNOWN_STABLECOINS = {
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC",
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": "USDT",
    "USDSwr9ApdHk5bvJKMjXLj5hTVfvamNHsLfFdrXKxXB": "USDS",
    "2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo": "PYUSD",
}

SOL_MINT = "So11111111111111111111111111111111"


def resolve_token_symbol(mint: str) -> str | None:
    if mint == SOL_MINT:
        return "SOL"
    return WELL_KNOWN_STABLECOINS.get(mint)
