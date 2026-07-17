#!/usr/bin/env bash
# run.sh — one-shot launcher for the copy bot
set -e

cd "$(dirname "$0")"

# Install deps if needed
if ! python3 -c "import aiohttp, eth_account, yaml" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

mkdir -p logs

case "${1:-}" in
    scan)
        echo "=== Scanning leaderboard for best ROI targets ==="
        python3 scanner.py "${@:2}"
        ;;
    scan-set)
        echo "=== Scanning + auto-updating config.yaml ==="
        python3 scanner.py --set
        ;;
    dry)
        echo "=== DRY RUN — logging only, no real orders ==="
        python3 -m app.main
        ;;
    live)
        echo "=== LIVE MODE — real orders will be placed ==="
        echo "WARNING: make sure polymarket: secrets are set in config.yaml"
        read -p "Confirm live trading? [y/N] " confirm
        [[ "$confirm" == "y" ]] || { echo "Aborted."; exit 1; }
        python3 -m app.main
        ;;
    *)
        echo "Usage: ./run.sh [scan|scan-set|dry|live]"
        echo ""
        echo "  scan      — fetch leaderboard, show top ROI traders"
        echo "  scan-set  — scan + auto-write best wallet to config.yaml"
        echo "  dry       — run bot in dry_run mode (safe, logs only)"
        echo "  live      — run bot with real order execution"
        echo ""
        echo "Quickstart:"
        echo "  ./run.sh scan          # see who to copy"
        echo "  ./run.sh dry           # confirm bot detects fills"
        echo "  # fill in polymarket: secrets in config.yaml"
        echo "  ./run.sh live          # go"
        ;;
esac
