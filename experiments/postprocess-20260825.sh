#!/bin/bash
# Waits for scale-20260825.sh to finish, then regenerates the mismatch
# drill-down and the contract-schema tables from the scale + SOTA data.
set -u
cd "$(dirname "$0")/.." || exit 1
PY=framework/venv/bin/python

while pgrep -f 'scale-20260825.sh' > /dev/null 2>&1; do
  sleep 60
done
echo "=== $(date -u +%FT%TZ) scale run finished; regenerating docs ==="

CHEAP_MAP="gemini=gemini-2.5-flash,openai=gpt-5-mini,anthropic=claude-haiku-4-5-20251001,deepseek=deepseek-v4-flash"
SOTA_MAP="gemini=gemini-3.1-pro-preview,openai=gpt-5.6-sol,anthropic=claude-fable-5,deepseek=deepseek-v4-pro"
# 08:00 captures the whole 25 Aug run (morning attempt + resumed relaunches).
SINCE="2026-08-25T08:00"
UNTIL="2026-08-27T00:00"

"$PY" experiments/render_drilldown.py \
  --input smoke=experiments/results/experiment_ii_llm.jsonl \
  --input scale=experiments/results/scale-20260825/ii/experiment_ii_llm.jsonl \
  --input sota=experiments/results/scale-20260825/sota/experiment_ii_llm.jsonl \
  --out experiments/results/mismatch-drilldown.md

"$PY" experiments/summarize_contract.py \
  --run "scale-cheap;experiments/results/scale-20260825/ii;${SINCE};${UNTIL};${CHEAP_MAP}" \
  --run "sota;experiments/results/scale-20260825/sota;${SINCE};${UNTIL};${SOTA_MAP}" \
  --run "i-synthesis;experiments/results/scale-20260825/i-synthesis;${SINCE};${UNTIL}" \
  --run "i-selection;experiments/results/scale-20260825/i-selection;${SINCE};${UNTIL}" \
  --out experiments/results/contract-tables.md

echo "=== $(date -u +%FT%TZ) postprocess done ==="
