#!/bin/zsh
# Run a sequence of experiments unattended, one after another, each capped by
# its own budget_eur. May be launched under a host supervisor via
# tools/launch_chain.sh (last resort; prefer a machine that is meant to run
# unattended). When the chain ends — success or failed legs — this script
# uninstalls that one-shot so login does not re-fire it.
#
#   tools/run_chain.sh 20260903-llm-decides-on-oracle-inputs-partial-specification 20260903-llm-only-plus-rules ...
#
# Logs: experiments/_chains/<timestamp>.log (plus each experiment's run.log).
# A failing experiment does not stop the chain; the chain log records it.
# Interrupted mid-run: the supervisor may stay so --resume can continue;
# clear leftovers with tools/unload_chain.sh.

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
# One-shot host jobs must not survive a finished chain (login would re-run them).
if [ -f "$(dirname "$0")/unload_chain.sh" ]; then
  sh "$(dirname "$0")/unload_chain.sh" | tee -a "$LOG" || true
fi
