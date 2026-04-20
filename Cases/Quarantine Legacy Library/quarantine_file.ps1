param(
    [Parameter(Mandatory=$true)]
    [string]$TargetFile,

    [string]$QuarantineDir = ".\quarantine",

    [bool]$DryRun = $false
)

# ------------------------------------------------------------
# quarantine_file.ps1
#
# Purpose:
# Safely move a file into a quarantine directory to test whether
# it is still required by the system.
#
# Usage examples:
#   .\quarantine_file.ps1 -TargetFile "C:\Temp\lib123.dll"
#   .\quarantine_file.ps1 -TargetFile "C:\Temp\lib123.dll" -QuarantineDir "C:\Quarantine"
#   .\quarantine_file.ps1 -TargetFile "C:\Temp\lib123.dll" -QuarantineDir "C:\Quarantine" -DryRun $true
# ------------------------------------------------------------

if (-not (Test-Path -Path $TargetFile -PathType Leaf)) {
    Write-Output "Target file not found: $TargetFile"
    exit 1
}

if (-not (Test-Path -Path $QuarantineDir)) {
    New-Item -ItemType Directory -Path $QuarantineDir -Force | Out-Null
}

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BaseName = Split-Path $TargetFile -Leaf
$QuarantinedFile = Join-Path $QuarantineDir "${Timestamp}_$BaseName"

if ($DryRun) {
    Write-Output "[DRY RUN] No changes will be made"
    Write-Output "Would move:"
    Write-Output "  From: $TargetFile"
    Write-Output "  To:   $QuarantinedFile"
    exit 0
}

Move-Item -Path $TargetFile -Destination $QuarantinedFile

Write-Output "File quarantined successfully"
Write-Output "Original: $TargetFile"
Write-Output "Quarantined: $QuarantinedFile"
Write-Output ""
Write-Output "Next Steps:"
Write-Output "- Monitor the system for errors or missing dependencies"
Write-Output "- If issues occur, restore using the rollback command below"
Write-Output ""
Write-Output "Rollback command:"
Write-Output "Move-Item -Path `"$QuarantinedFile`" -Destination `"$TargetFile`""