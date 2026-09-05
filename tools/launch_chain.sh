#!/bin/zsh
# Launch tools/run_chain.sh as a one-shot launchd user agent so it survives the
# launching shell (Cursor terminals die with the client). Usage:
#
#   tools/launch_chain.sh 20260903-llm-decides-on-oracle-inputs-partial-specification 20260903-llm-only-plus-rules
#
# Status:  launchctl list | grep statute-decider
# Stop:    launchctl bootout gui/$(id -u)/com.ottomattas.statute-decider.chain
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
