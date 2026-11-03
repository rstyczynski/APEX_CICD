([.labels[].name] | unique) as $labels |
if .user.login == "github-actions[bot]" and (.head.ref | startswith("release-please--"))
   and ($labels | index("autorelease: pending")) then "generated release PR"
else
  [$labels[] | select(. == "patch" or . == "minor" or . == "major")] as $levels |
  if ($levels | length) != 1 then error("Choose exactly one patch/minor/major label")
  else $levels[0] as $level |
    {patch:"^fix(\\([^\\r\\n)]+\\))?: ", minor:"^feat(\\([^\\r\\n)]+\\))?: ", major:"^feat(\\([^\\r\\n)]+\\))?!: "}[$level] as $prefix |
    if (.title | test($prefix + "\\S[^\\r\\n]*$")) then $level
    else error("Label requires matching Conventional Commit title") end
  end
end
