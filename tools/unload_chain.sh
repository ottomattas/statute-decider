#!/bin/sh
# Remove the one-shot experiment-chain job if a host supervisor was used.
# Safe to run when nothing is registered. macOS: launchctl + LaunchAgent plist.
# Linux: no unit is installed by launch_chain.sh today (no-op).
#
#   tools/unload_chain.sh
#
# Label override: ES_CHAIN_LABEL (default com.ottomattas.statute-decider.chain).

set -eu
LABEL="${ES_CHAIN_LABEL:-com.ottomattas.statute-decider.chain}"

if command -v launchctl >/dev/null 2>&1 && [ "$(uname -s)" = Darwin ]; then
  launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
  rm -f "$HOME/Library/LaunchAgents/$LABEL.plist"
  echo "unloaded $LABEL"
  exit 0
fi

echo "no host supervisor to unload on this platform ($LABEL)"
