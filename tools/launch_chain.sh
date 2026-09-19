#!/bin/zsh
# Last-resort host one-shot: run tools/run_chain.sh under a macOS LaunchAgent
# so it survives the IDE shell. Prefer a cloud/HPC/CI runner when the work
# does not need this machine. run_chain.sh uninstalls this job when the
# chain ends; an interrupted leftover is tools/unload_chain.sh.
#
#   tools/launch_chain.sh 20260903-llm-decides-on-oracle-inputs-partial-specification 20260903-llm-only-plus-rules
#
# Status:  launchctl print gui/$(id -u)/com.ottomattas.statute-decider.chain
# Stop:    tools/unload_chain.sh
# Log:     tail -f experiments/_chains/*.log

set -eu
REPO="$(cd "$(dirname "$0")/.." && pwd)"
LABEL="com.ottomattas.statute-decider.chain"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
mkdir -p "$HOME/Library/LaunchAgents" "$REPO/experiments/_chains"

# Remove a previous instance of the job if one is still registered.
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true

{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
  echo '<plist version="1.0"><dict>'
  echo "  <key>Label</key><string>$LABEL</string>"
  echo '  <key>ProgramArguments</key><array>'
  echo "    <string>$REPO/tools/run_chain.sh</string>"
  for exp in "$@"; do echo "    <string>$exp</string>"; done
  echo '  </array>'
  echo "  <key>WorkingDirectory</key><string>$REPO</string>"
  echo '  <key>RunAtLoad</key><true/>'
  echo '  <key>KeepAlive</key><false/>'
  echo "  <key>StandardOutPath</key><string>$REPO/experiments/_chains/launchd.out</string>"
  echo "  <key>StandardErrorPath</key><string>$REPO/experiments/_chains/launchd.err</string>"
  echo '  <key>EnvironmentVariables</key><dict>'
  echo '    <key>PATH</key><string>/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin</string>'
  echo "    <key>HOME</key><string>$HOME</string>"
  echo '  </dict>'
  echo '</dict></plist>'
} > "$PLIST"

launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "launched $LABEL with: $*"
echo "log dir: $REPO/experiments/_chains"
echo "WARN: host-persistent one-shot. It must uninstall at chain end; leftover → tools/unload_chain.sh"
