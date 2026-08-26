#!/bin/bash
# Scale run 25 Aug 2026 (JURIX sprint). Four sequential legs, one shared EUR
# ledger and one FRAMEWORK_BUDGET_EUR=100 cap (the harness ingests prior
# ledger spend on every leg, so the cap is cumulative across legs).
# Launch: nohup bash experiments/scale-20260825.sh > experiments/scale-20260825.log 2>&1 &
set -u
cd "$(dirname "$0")/.." || exit 1
PY=framework/venv/bin/python

# Resume semantics: rows already recorded (results JSONL, or cost ledger at/
# after this timestamp) are skipped — append-only, no re-spend. Covers the
# 2026-08-25 morning + afternoon attempts of this same run id.
RESUME_SINCE=2026-08-25T00:00:00Z

leg() {
  local name="$1" config="$2" results="$3"
  echo "=== $(date -u +%FT%TZ) START leg=${name} config=${config} ==="
  "$PY" framework/run_experiments.py --config "$config" --results-dir "$results" \
    --resume-since "$RESUME_SINCE"
  echo "=== $(date -u +%FT%TZ) END leg=${name} exit=$? ==="
}

leg ii          experiments/matrix-scale-ii.yaml          experiments/results/scale-20260825/ii
leg i-synthesis experiments/matrix-scale-i-synthesis.yaml experiments/results/scale-20260825/i-synthesis
leg i-selection experiments/matrix-scale-i-selection.yaml experiments/results/scale-20260825/i-selection

export FRAMEWORK_GEMINI_MODEL=gemini-3.1-pro-preview
export FRAMEWORK_OPENAI_MODEL=gpt-5.6-sol
export FRAMEWORK_ANTHROPIC_MODEL=claude-fable-5
export FRAMEWORK_DEEPSEEK_MODEL=deepseek-v4-pro
leg sota        experiments/matrix-sota.yaml              experiments/results/scale-20260825/sota

echo "=== $(date -u +%FT%TZ) ALL LEGS DONE ==="
