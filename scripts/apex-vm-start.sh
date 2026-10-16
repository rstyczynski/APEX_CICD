#!/usr/bin/env bash
# Use launchd so the VM outlives the terminal/automation session that starts it.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .local-apex
label=local.apex-cicd.vm-start
domain="gui/$(id -u)"
cat > .local-apex/vm-start.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "https://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>$label</string>
<key>ProgramArguments</key><array><string>/opt/homebrew/bin/podman</string><string>machine</string><string>start</string><string>apex-cicd</string></array>
<key>EnvironmentVariables</key><dict><key>CONTAINERS_CONF_OVERRIDE</key><string>$PWD/.local-apex/containers.conf</string><key>PATH</key><string>/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin</string></dict>
<key>WorkingDirectory</key><string>$PWD</string>
<key>StandardOutPath</key><string>$PWD/.local-apex/vm-start.log</string>
<key>StandardErrorPath</key><string>$PWD/.local-apex/vm-start.log</string>
<key>RunAtLoad</key><true/>
<key>AbandonProcessGroup</key><true/>
</dict></plist>
EOF
launchctl bootout "$domain/$label" 2>/dev/null || true
launchctl bootstrap "$domain" "$PWD/.local-apex/vm-start.plist"
for ((attempt=0; attempt<90; attempt++)); do
  if podman --connection apex-cicd info >/dev/null 2>&1; then
    echo 'APEX VM ready (launched independently through launchd).'
    exit 0
  fi
  sleep 2
done
cat .local-apex/vm-start.log
exit 1
