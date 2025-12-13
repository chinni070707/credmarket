# Script to install Git hooks (PowerShell version)

$HOOKS_DIR = ".git/hooks"
$SCRIPT_DIR = $PSScriptRoot

Write-Host "Installing Git hooks..." -ForegroundColor Cyan

# Copy pre-push hook (bash version)
if (Test-Path "$SCRIPT_DIR\.git\hooks\pre-push") {
    Copy-Item "$SCRIPT_DIR\.git\hooks\pre-push" "$HOOKS_DIR\pre-push" -Force
    Write-Host "✅ Installed pre-push hook (bash)" -ForegroundColor Green
}

# Copy pre-push hook (PowerShell version)
if (Test-Path "$SCRIPT_DIR\.git\hooks\pre-push.ps1") {
    Copy-Item "$SCRIPT_DIR\.git\hooks\pre-push.ps1" "$HOOKS_DIR\pre-push.ps1" -Force
    Write-Host "✅ Installed pre-push hook (PowerShell)" -ForegroundColor Green
}

Write-Host ""
Write-Host "Git hooks installed successfully!" -ForegroundColor Green
Write-Host "Tests will now run automatically before each push." -ForegroundColor Yellow
