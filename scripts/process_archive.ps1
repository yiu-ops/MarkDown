# PowerShell Script to Process Archive Regulations
# This script automates the workflow:
# 1. Finds the latest .docx file in the archive folder
# 2. Converts it to markdown using Pandoc
# 3. Runs the python script to split and update regulations
# 4. Opens the update report

# Set encoding
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Get script directory and project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
$archiveDir = Join-Path $projectRoot "archive"
$outputMd = Join-Path $archiveDir "output.md"
$pythonScript = Join-Path $scriptDir "split_and_update.py"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   Regulation Archive Processing System" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Find latest docx file
$latestDocx = Get-ChildItem -Path $archiveDir -Filter *.docx | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $latestDocx) {
    Write-Error "No .docx files found in $archiveDir"
    exit 1
}

Write-Host "`n[1] Found latest archive file:" -ForegroundColor Yellow
Write-Host "    $($latestDocx.Name) ($($latestDocx.LastWriteTime))" -ForegroundColor White

# 2. Convert to Markdown using Pandoc
Write-Host "`n[2] Converting to Markdown (Pandoc)..." -ForegroundColor Yellow

if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Error "Pandoc is not installed or not in PATH."
    exit 1
}

try {
    # Run pandoc
    pandoc -f docx -t markdown "$($latestDocx.FullName)" -o "$outputMd"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    Conversion successful: $outputMd" -ForegroundColor Green
    }
    else {
        Write-Error "    Pandoc conversion failed with exit code $LASTEXITCODE"
        exit 1
    }
}
catch {
    Write-Error "    Error running Pandoc: $_"
    exit 1
}

# 3. Run Python script to split and update
Write-Host "`n[3] Splitting and Updating Regulations..." -ForegroundColor Yellow

try {
    python "$pythonScript" "$outputMd"
}
catch {
    Write-Error "    Failed to run Python script: $_"
    exit 1
}

# 4. Check for report
$reportPath = Join-Path $projectRoot "update_report.html"
if (Test-Path $reportPath) {
    Write-Host "`n[4] Update Report Generated!" -ForegroundColor Green
    Write-Host "    Opening report..." -ForegroundColor White
    Invoke-Item "$reportPath"
}
else {
    Write-Host "`n[4] No changes detected (no report generated)." -ForegroundColor Gray
}

Write-Host "`nDone." -ForegroundColor Cyan
