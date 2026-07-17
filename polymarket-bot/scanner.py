#!/usr/bin/env python3
"""
scanner.py — Polymarket leaderboard scanner.

Fetches top traders, ranks by ROI, checks recent activity,
and outputs config-ready wallet recommendations.

Usage:
    python scanner.py              # top 10 by ROI
    python scanner.py --limit 50  # wider search
    python scanner.py --set       # auto-write best wallet to config.yaml
"""

import argparse
import asyncio
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import aiohttp
import yaml

LEADERBOARD_URL = "https://data-api.polymarket.com/v1/leaderboard"
ACTIVITY_URL    = "https://data-api.polymarket.com/v1/activity"
POSITIONS_URL   = "https://data-api.polymarket.com/v1/positions"
CONFIG_FILE     = Path(__file__).parent / "config.yaml"

# Min absolute PnL to filter noise
MIN_PNL = 5_000
# Min volume to filter zero-vol anomalies
MIN_VOL = 1_000
# Consider "active" if they traded in the last N days
ACTIVE_DAYS = 30


async def fetch_json(session: aiohttp.ClientSession, url: str, params: dict) -> list | dict:
    async with session.get(url, params=params) as r:
        r.raise_for_status()
        return await r.json()


async def last_trade_days_ago(session: aiohttp.ClientSession, wallet: str) -> float | None:
    """Return days since last trade, or None if no trades found."""
    try:
        data = await fetch_json(session, ACTIVITY_URL, {"user": wallet, "limit": 5})
        trades = [e for e in data if e.get("type") == "TRADE"]
        if not trades:
            return None
        latest_ts = max(t["timestamp"] for t in trades)
        elapsed = time.time() - latest_ts
        return elapsed / 86400
    except Exception:
        return None


async def scan(limit: int = 100) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        print(f"Fetching top {limit} traders from Polymarket leaderboard...")
        raw = await fetch_json(session, LEADERBOARD_URL, {
            "limit": limit,
            "interval": "all",
            "sortBy": "profitAndLoss",
        })

        candidates = []
        for t in raw:
            pnl = float(t.get("pnl", 0))
            vol = float(t.get("vol", 0))
            if pnl < MIN_PNL or vol < MIN_VOL:
                continue
            roi = pnl / vol
            candidates.append({
                "rank":    int(t["rank"]),
                "wallet":  t["proxyWallet"],
                "name":    t.get("userName", ""),
                "pnl":     pnl,
                "vol":     vol,
                "roi":     roi,
            })

        # Sort by ROI descending
        candidates.sort(key=lambda x: x["roi"], reverse=True)

        print(f"Checking activity for top {min(20, len(candidates))} ROI candidates...")
        top = candidates[:20]
        tasks = [last_trade_days_ago(session, c["wallet"]) for c in top]
        ages = await asyncio.gather(*tasks)

        for c, age in zip(top, ages):
            c["days_since_trade"] = age
            c["active"] = age is not None and age <= ACTIVE_DAYS

        return top


def print_table(traders: list[dict]) -> None:
    print()
    print(f"{'#':>4}  {'Name':<28}  {'PnL':>10}  {'Vol':>12}  {'ROI':>7}  {'Last Trade':>12}  Active")
    print("-" * 90)
    for i, t in enumerate(traders, 1):
        age = f"{t['days_since_trade']:.1f}d ago" if t["days_since_trade"] is not None else "unknown"
        flag = "YES" if t["active"] else "---"
        print(
            f"{i:>4}  {t['name']:<28}  "
            f"${t['pnl']:>9,.0f}  "
            f"${t['vol']:>11,.0f}  "
            f"{t['roi']:>6.1%}  "
            f"{age:>12}  {flag}"
        )
    print()


def best_active(traders: list[dict]) -> dict | None:
    for t in traders:
        if t["active"]:
            return t
    return None


def set_config_wallet(wallet: str, name: str) -> None:
    cfg = yaml.safe_load(CONFIG_FILE.read_text())
    cfg["target_wallet"] = wallet
    CONFIG_FILE.write_text(
        f"# target updated by scanner.py — {name} ({wallet})\n"
        + yaml.dump(cfg, default_flow_style=False, allow_unicode=True)
    )
    print(f"config.yaml updated → {name} ({wallet})")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Polymarket leaderboard ROI scanner")
    parser.add_argument("--limit", type=int, default=100, help="Traders to fetch (default 100)")
    parser.add_argument("--set", action="store_true", help="Write best active wallet to config.yaml")
    args = parser.parse_args()

    traders = await scan(args.limit)
    print_table(traders)

    best = best_active(traders)
    if best:
        print(f"Best active target: {best['name']} ({best['wallet']})")
        print(f"  ROI: {best['roi']:.1%}  |  PnL: ${best['pnl']:,.0f}  |  Last trade: {best['days_since_trade']:.1f}d ago")
        if args.set:
            set_config_wallet(best["wallet"], best["name"])
        else:
            print(f"\nTo use this wallet: python scanner.py --set")
            print(f"Or manually set target_wallet in config.yaml")
    else:
        print("No active traders found in top results. Try --limit 200.")


if __name__ == "__main__":
    asyncio.run(main())
