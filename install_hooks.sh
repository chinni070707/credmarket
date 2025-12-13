#!/bin/bash
# Script to install Git hooks

HOOKS_DIR=".git/hooks"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Git hooks..."

# Copy pre-push hook
if [ -f "$SCRIPT_DIR/.git/hooks/pre-push" ]; then
    cp "$SCRIPT_DIR/.git/hooks/pre-push" "$HOOKS_DIR/pre-push"
    chmod +x "$HOOKS_DIR/pre-push"
    echo "✅ Installed pre-push hook (bash)"
fi

if [ -f "$SCRIPT_DIR/.git/hooks/pre-push.ps1" ]; then
    cp "$SCRIPT_DIR/.git/hooks/pre-push.ps1" "$HOOKS_DIR/pre-push.ps1"
    echo "✅ Installed pre-push hook (PowerShell)"
fi

echo ""
echo "Git hooks installed successfully!"
echo "Tests will now run automatically before each push."
