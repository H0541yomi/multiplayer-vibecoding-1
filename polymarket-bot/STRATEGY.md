# Polymarket Copycat Strategy — Final Edition
**Research basis: 23-strategy tournament, 8+ deep-research agents, 6-month walk-forward, filter attribution analysis**
**Compiled: 2026-07-17**

---

## The Honest Summary

This strategy works — but it is not a money printer. It has catastrophic months.
Read this before deploying real capital.

**Best 30-day backtest:** +161–171% ROI
**6-month compound:** -77.5% (3 of 6 months profitable)
**Core edge:** Real, but episodic. Requires active monthly oversight to not blow up.

---

## What the Edge Actually Is

Both top copy targets (Hauchn, ostintheell) trade **one specific market niche**:
*"Will X be the largest company in the world by market cap on [date]?"* markets
for Apple, NVIDIA, Alphabet, Amazon.

The edge: these markets misprice the true probability of a company holding or losing
its #1 rank. Hauchn and ostintheell repeatedly buy outcomes at 5–15¢ that should
be priced at 20–35¢ as resolution approaches. The move from 10¢ → 30¢ is a 3x.

**Why it works specifically at 5–15¢ entry:**
- Below 5¢: noise, near-zero upside even if right
- 5–15¢: genuine mispricing window, 2–5x upside to resolution
- Above 20¢: consistently losing across both wallets (-84% to -99%)

**Entry price is the entire strategy.** Every other filter (time of day, conviction
threshold, market category) adds less than 2.5pp of ROI in attribution testing.

---

## Primary Target

**Hauchn** — `0xf0ca28d5b0141f0a8e7b251dea80fd881cb166ed`

- All-time leaderboard ROI: **165%** ($75k PnL on $46k vol)
- 9 unique markets across 347 trades in the last 30 days
- Strategy: buys market-cap ranking outcomes 5–15¢, holds to resolution (~39 days)
- Peak trading hour: 13–15 UTC (US pre-market) — 53% of trades
- Best single position: Apple market cap YES, 7¢ → 27¢, +$1,613 P&L

**Secondary:** ostintheell (`0xb0c85813a7a4428f1139ff91d3118a92c391fe7f`)
trades the same markets. Use as confirmation signal, not independent diversification.
**Do not blend them** — they are the same bet.

---

## Entry Rules

| Rule | Value | Evidence |
|------|-------|----------|
| Entry price | **5¢ – 15¢** | Load-bearing filter: +107.6pp ROI vs unfiltered |
| Market type | Market-cap ranking | Both wallets: 100% of this niche |
| Copy size | **5–20% of target fill** | 20% = max P&L, higher = capital risk |
| Order type | **Maker (limit)** | ~0.5% vs 3% taker slippage, ~+10pp ROI |
| Max open positions | **$3,000 USDC (starting)** | Hard cap until 3 profitable months verified |

**Do not filter by time of day** — attribution test showed 0.0pp independent contribution.
**Do not filter by conviction count** — 96.6% of trades already pass the 20+ threshold.

---

## The Real Performance Record (6-Month Walk-Forward)

| Period | Monthly ROI | Context |
|--------|-------------|---------|
| Jan–Feb 2026 | **-84.3%** | Catastrophic. 549 trades, 385 entries, heavy accumulation into losing positions |
| Feb–Mar 2026 | +33.0% | Recovery begins |
| Mar–Apr 2026 | **-33.6%** | Drawdown resumes |
| Apr–May 2026 | +50.2% | Strong recovery |
| May–Jun 2026 | +40.6% | Continued recovery |
| Jun–Jul 2026 | -23.1% | Current month (partial) |
| **6-month compound** | **-77.5%** | Undiversified, no stop-loss |
| **30-day (last window)** | **+161%** | What the initial backtest found |

**The 30-day backtest is not a lie.** The last 30 days genuinely performed at +161%.
But the 6-month picture shows this strategy has months that can wipe 80%+ of capital.
**Without a stop-loss, this strategy destroys capital over 6 months.**

---

## Mandatory Risk Management

These are not suggestions. Without them, the January 2026 month repeats.

### Monthly Stop-Loss (Hard Rule)
- At the start of each month, note your capital.
- If down **>25% within any rolling 30-day period**, **stop copying immediately**.
- Resume only after Hauchn shows a profitable 7-day window.

### Position Size Discipline
- Start at **5% copy size**, not 20%.
- Scale to 10% after 1 profitable month. Scale to 20% after 3 profitable months.
- Never exceed 20% copy size regardless of confidence.

### When to Pause
- Hauchn shows no trades for >7 days → pause, run `scanner.py --set`
- Monthly loss exceeds 25% → pause
- Hauchn's all-time ROI drops from leaderboard top 10 → investigate before resuming

### Capital Allocation
Do not deploy your entire trading capital into this strategy.
The 6-month -77.5% result means it can lose most of what you put in.
Treat this as a high-risk allocation: size it like a venture bet, not a savings account.

---

## The Three Active Markets (July 2026)

Based on Hauchn's current open positions:

| Market | Entry | Current | Return | Status |
|--------|-------|---------|--------|--------|
| NVIDIA #1 market cap (July 31) | $0.099 | $0.295 | +174% | 🟢 Open |
| Apple #1 market cap (July 31) | $0.052 | $0.270 | +275% | 🟢 Open |
| Alphabet #1 market cap (July 31) | $0.039 | $0.024 | -57% | 🔴 Losing |

**Copy NVIDIA and Apple positions. Skip Alphabet.** Alphabet has been the consistent
loser in this niche across both Hauchn and ostintheell.

---

## What the Tournament Eliminated

23 strategies tested across 10+ wallets. Everything except Hauchn's core edge failed:

| Wallet | Result | Why |
|--------|--------|-----|
| ChristmasCracker | -21.6% | Long-tail spray; stale open book |
| donthackme | +391% claimed, **disqualified** | All 52 trades in last 7 days only |
| godblessme2026 | +349% claimed, **disqualified** | Wallet has zero trade history |
| Kingdmandan | -91.5% | 7 trades, 0 wins in 30-day test |
| needheal | -8.2% | 94 trades, 0 wins |
| BreakTheBank | -7.1% | Negative on fresh entries |
| TAIWANNUMBERONE | -62.4% | $3,839 loss on $6,148 deployed |
| yesmamaok | -98.0% | Esports specialist, all resolved to 0 |
| 0x34d1 | -100.0% | All-in on Switzerland winning World Cup |
| rangnihui | -61.1% | 489 trades, 0 wins |
| ostintheell | +114.5% claimed → **-69.7% realized** | Same trade as Hauchn; MTM inflation |

---

## Operational Playbook

### Setup
```bash
cd ~/Documents/random/polymarket-bot

# Install dependencies
pip install -r requirements.txt

# Verify bot detects Hauchn's trades (watch for 2+ minutes)
./run.sh dry
# Expect: "Subscribed target: 0xf0ca28d5b0141f0a8e7b251dea80fd881cb166ed"
```

### Going Live
```bash
# 1. Edit config.yaml — uncomment polymarket: block
#    Credentials from: polymarket.com → Settings → API Keys

# 2. Start with 5% copy size (not 20%)
#    Change sizing.percent_of_target: 0.05

# 3. Fund Polygon wallet with your starting USDC
#    Min recommended: $500 (enough to copy at 5% across 5-10 positions)

# 4. Run dry_run for 48h, confirm fills appear in logs
tail -f logs/tracecopy.log

# 5. Switch to real
./run.sh live
```

### Weekly Check (5 minutes)
```bash
# Check if Hauchn is still active
curl "https://data-api.polymarket.com/v1/activity?user=0xf0ca28d5b0141f0a8e7b251dea80fd881cb166ed&limit=5"

# Refresh leaderboard, auto-rotate if better target found
./run.sh scan

# Review P&L — calculate rolling 30-day return
# If down >25%: stop bot, investigate
```

### Monthly Review
1. Calculate net P&L for the month
2. If profitable: consider scaling up copy size by 5pp
3. If down >25%: stop immediately per stop-loss rule
4. Re-run scanner to confirm Hauchn still in top 10 by ROI

---

## Config (Current Best)

```yaml
target_wallet: "0xf0ca28d5b0141f0a8e7b251dea80fd881cb166ed"
mode: dry_run  # change to: real

sizing:
  mode: percent_of_target
  percent_of_target: 0.05  # start here; scale to 0.20 after 3 profitable months
  max_usd_total_in_positions: 3000.0
  min_target_shares_to_copy: 10

execution:
  order_type: maker  # lower slippage; ~0.5% vs 3%

slippage:
  entry_bps_max: 50

# Credentials — get from polymarket.com → Settings → API Keys
#polymarket:
#  private_key: "0x..."
#  wallet_address: "0x..."
#  api_key: "..."
#  api_secret: "..."
#  passphrase: "..."
```

---

## Summary

The edge is **real but narrow**: buy market-cap ranking outcomes at 5–15¢ alongside
Hauchn, hold to resolution. The entry price filter is the entire strategy — everything
else is noise.

The risk is **real and severe**: three of six months in 2026 were deeply negative.
A January 2026 repeat would wipe 80% of deployed capital without a stop-loss.

**Treat this as:** a high-variance, active-management strategy with genuine alpha
in the right conditions — not passive income. Size it accordingly. Stop when the
rules say stop. The discipline is the strategy.
