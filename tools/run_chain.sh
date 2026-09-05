#!/bin/zsh
# Run a sequence of experiments unattended, one after another, each capped by
# its own budget_eur. Meant to be launched under launchd (survives the IDE
# shell going away) via tools/launch_chain.sh.
#
#   tools/run_chain.sh 20260903-llm-decides-on-oracle-inputs-partial-specification 20260903-llm-only-plus-rules ...
#
# Logs: experiments/_chains/<timestamp>.log (plus each experiment's run.log).
# A failing experiment does not stop the chain; the chain log records it.

set -u
cd "$(dirname "$0")/.." || exit 1
mkdir -p experiments/_chains
STAMP=$(date +%Y%m%d-%H%M%S)
LOG="experiments/_chains/${STAMP}.log"

echo "chain start $(date -Iseconds) commit $(git rev-parse --short HEAD)" | tee -a "$LOG"
for exp in "$@"; do
  echo "=== $exp start $(date -Iseconds)" | tee -a "$LOG"
  # --resume makes the chain idempotent: a finished experiment has nothing
  # pending and is skipped; an interrupted one continues from its rows.jsonl.
  if .venv/bin/sd run --experiment "experiments/$exp" --execution parallel --models all --resume >> "$LOG" 2>&1; then
    echo "=== $exp done  $(date -Iseconds)" | tee -a "$LOG"
  else
    echo "=== $exp FAILED (exit $?) $(date -Iseconds)" | tee -a "$LOG"
  fi
  grep -h 'done:' "experiments/$exp/results/run.log" 2>/dev/null | tail -1 | tee -a "$LOG"
done
echo "chain end $(date -Iseconds)" | tee -a "$LOG"
