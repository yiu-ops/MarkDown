# PowerShell Script to Copy Regulation Files with Korean Names
# This script reads regulations.json and copies all regulation markdown files
# from their coded names (e.g., 3-2-11.md) to meaningful Korean names (e.g., 보수지급규정.md)

# Set encoding to UTF-8 for Korean characters
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Get the script directory and project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

# Define paths
$jsonPath = Join-Path $projectRoot "regulations.json"
$outputDir = Join-Path $projectRoot "regulations_for_rag"

# Check if regulations.json exists
if (-not (Test-Path $jsonPath)) {
    Write-Error "regulations.json not found at: $jsonPath"
    exit 1
}

# Create output directory if it doesn't exist
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
    Write-Host "Created output directory: $outputDir" -ForegroundColor Green
}

# Read and parse JSON
Write-Host "`nReading regulations.json..." -ForegroundColor Cyan
$jsonContent = Get-Content -Path $jsonPath -Raw -Encoding UTF8
$data = $jsonContent | ConvertFrom-Json

# Counter for statistics
$successCount = 0
$failCount = 0
$skippedCount = 0

Write-Host "Found $($data.total_regulations) regulations in JSON`n" -ForegroundColor Cyan
Write-Host "Copying files with Korean names..." -ForegroundColor Yellow
Write-Host ("=" * 80) -ForegroundColor Gray

# Process each regulation
foreach ($regulation in $data.regulations) {
    $sourceFile = Join-Path $projectRoot $regulation.path
    $koreanFileName = "$($regulation.title_normalized).md"
    $destinationFile = Join-Path $outputDir $koreanFileName
    
    # Check if source file exists
    if (Test-Path $sourceFile) {
        try {
            # Copy the file
            Copy-Item -Path $sourceFile -Destination $destinationFile -Force
            
            # Display progress
            $sourceFileName = Split-Path -Leaf $sourceFile
            Write-Host "[✓] " -ForegroundColor Green -NoNewline
            Write-Host "$sourceFileName " -ForegroundColor White -NoNewline
            Write-Host "→ " -ForegroundColor Yellow -NoNewline
            Write-Host "$koreanFileName" -ForegroundColor Cyan
            
            $successCount++
        }
        catch {
            Write-Host "[✗] Failed to copy: $($regulation.code) - $($_.Exception.Message)" -ForegroundColor Red
            $failCount++
        }
    }
    else {
        Write-Host "[!] Source file not found: $sourceFile" -ForegroundColor Yellow
        $skippedCount++
    }
}

# Display summary
Write-Host "`n" ("=" * 80) -ForegroundColor Gray
Write-Host "`nSummary:" -ForegroundColor Cyan
Write-Host "  ✓ Successfully copied: $successCount files" -ForegroundColor Green
if ($failCount -gt 0) {
    Write-Host "  ✗ Failed: $failCount files" -ForegroundColor Red
}
if ($skippedCount -gt 0) {
    Write-Host "  ! Skipped (not found): $skippedCount files" -ForegroundColor Yellow
}
Write-Host "`nOutput directory: $outputDir" -ForegroundColor Cyan

# List all files in output directory
Write-Host "`nFiles in output directory:" -ForegroundColor Cyan
Get-ChildItem -Path $outputDir -Filter *.md | Sort-Object Name | ForEach-Object {
    Write-Host "  - $($_.Name)" -ForegroundColor White
}

Write-Host "`n✓ Done! All files are ready for RAG system upload." -ForegroundColor Green
