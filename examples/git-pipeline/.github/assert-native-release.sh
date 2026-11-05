# Source from a clean application checkout before packaging or target writes.
assert_native_release() {
  local version="$1"
  [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || return 1
  test "$(cat version.txt)" = "$version" || return 1
  jq -e --arg version "$version" '.lastReleaseVersion == $version' \
    .dbtools/project.config.json > /dev/null || return 1
  test -s "dist/releases/$version/release.changelog.xml" || return 1
  test -z "$(git status --porcelain --untracked-files=normal)" || return 1
}
