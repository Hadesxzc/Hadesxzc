# Fill GitHub contribution graph with backdated empty commits
# Adjust $startDate and $endDate to control the range
# Adjust $commitsPerDay for intensity (1-4 recommended)

$startDate = (Get-Date).AddDays(-365)  # 1 year ago
$endDate = (Get-Date).AddDays(-1)       # yesterday
$commitsPerDay = 1                       # commits per day (more = darker green)

# Optional: skip some days randomly to look more natural
$skipChance = 0.15  # 15% chance to skip a day (set to 0 for no skipping)

$current = $startDate
while ($current -le $endDate) {
    # Random skip to look natural
    if ((Get-Random -Minimum 0.0 -Maximum 1.0) -lt $skipChance) {
        $current = $current.AddDays(1)
        continue
    }

    # Random number of commits (1 to $commitsPerDay)
    $numCommits = Get-Random -Minimum 1 -Maximum ($commitsPerDay + 1)
    
    for ($i = 0; $i -lt $numCommits; $i++) {
        $hour = Get-Random -Minimum 9 -Maximum 22
        $minute = Get-Random -Minimum 0 -Maximum 59
        $dateStr = $current.ToString("yyyy-MM-ddT") + "{0:D2}:{1:D2}:00" -f $hour, $minute
        
        $env:GIT_AUTHOR_DATE = $dateStr
        $env:GIT_COMMITTER_DATE = $dateStr
        
        git commit --allow-empty -m "update: $($current.ToString('yyyy-MM-dd')) #$($i+1)"
    }

    $current = $current.AddDays(1)
}

# Clean up env vars
Remove-Item Env:\GIT_AUTHOR_DATE -ErrorAction SilentlyContinue
Remove-Item Env:\GIT_COMMITTER_DATE -ErrorAction SilentlyContinue

Write-Host "`nDone! Now run: git push" -ForegroundColor Green
