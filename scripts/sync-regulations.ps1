$ErrorActionPreference = "Stop"

$source = "regulations"
$dest = "docs"

Write-Host "Syncing regulations to docs/..."

# Ensure destination exists
if (-not (Test-Path $dest)) {
    New-Item -ItemType Directory -Path $dest | Out-Null
}

# Backup existing docs (only if backup doesn't exist)
if (-not (Test-Path "docs.backup")) {
    if (Test-Path $dest) {
        Write-Host "Backing up docs..."
        Copy-Item -Path $dest -Destination "docs.backup" -Recurse
    }
}

# Clear destination
Remove-Item -Path "$dest/*" -Recurse -Force

# Copy regulations
Get-ChildItem -Path $source -Directory | ForEach-Object {
    $dirName = $_.Name
    # Remove numeric prefix (e.g., "1-General" -> "General")
    $newName = $dirName -replace '^\d+-', ''
    
    $newDir = Join-Path $dest $newName
    New-Item -ItemType Directory -Path $newDir -Force | Out-Null
    
    # Process subdirectories
    Get-ChildItem -Path $_.FullName -Directory | ForEach-Object {
        $subDirName = $_.Name
        $subNewName = $subDirName -replace '^\d+-', ''
        $subNewDir = Join-Path $newDir $subNewName
        
        New-Item -ItemType Directory -Path $subNewDir -Force | Out-Null
        
        # Copy files from subdirectory
        Copy-Item -Path "$($_.FullName)\*" -Destination $subNewDir -Recurse
    }
    
    # Copy files from current directory (excluding subdirectories which are already handled)
    Get-ChildItem -Path $_.FullName -File | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $newDir
    }
}

# Create intro.md
if (Test-Path "docs.backup/intro.md") {
    Copy-Item "docs.backup/intro.md" "$dest/intro.md"
}
else {
    Set-Content "$dest/intro.md" "# 용인대학교 규정집`n`n용인대학교 제규정 통합 관리 시스템입니다." -Encoding UTF8
}

Write-Host "Sync completed!"
