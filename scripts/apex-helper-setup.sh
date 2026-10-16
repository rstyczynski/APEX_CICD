#!/usr/bin/env bash
# Project-local workaround for Podman 6.0 + krunkit 1.1.1 on this Mac.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .local-apex/helper
curl -fL --retry 3 -o .local-apex/krunkit-1.3.2.tgz \
  https://github.com/libkrun/krunkit/releases/download/v1.3.2/krunkit-podman-unsigned-1.3.2.tgz
printf '%s  %s\n' de9ab62dd90461cd1df1e37b78e780690d75490f4bab1674cbb4a1f75b90c227 \
  .local-apex/krunkit-1.3.2.tgz | shasum -a 256 -c -
tar -xzf .local-apex/krunkit-1.3.2.tgz -C .local-apex/helper
cat > .local-apex/krunkit-entitlements.plist <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "https://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>com.apple.security.hypervisor</key><true/>
</dict></plist>
EOF
install_name_tool -add_rpath '@executable_path/../lib' .local-apex/helper/bin/krunkit
for lib in .local-apex/helper/lib/*.dylib; do
  codesign --force --sign - "$lib"
done
codesign --force --sign - --entitlements .local-apex/krunkit-entitlements.plist \
  .local-apex/helper/bin/krunkit
printf '[engine]\nhelper_binaries_dir = ["%s/.local-apex/helper/bin", "/opt/homebrew/opt/podman/libexec/podman", "/opt/homebrew/bin"]\n' \
  "$PWD" > .local-apex/containers.conf
.local-apex/helper/bin/krunkit --version
