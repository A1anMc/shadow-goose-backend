#!/bin/bash

# 🔍 Dependency Conflict Checker
# This script checks for dependency conflicts and outdated packages

set -e

echo "🔍 Checking for dependency conflicts and outdated packages..."
echo "=================================================="

# Check for dependency conflicts
echo "1. Checking for dependency conflicts..."
if pip check; then
    echo "✅ No dependency conflicts found"
else
    echo "❌ Dependency conflicts detected!"
    echo "Please resolve conflicts before proceeding"
    exit 1
fi

# Check for outdated packages
echo ""
echo "2. Checking for outdated packages..."
echo "Outdated packages:"
pip list --outdated || echo "No outdated packages found"

# Generate dependency tree
echo ""
echo "3. Generating dependency tree..."
if command -v pipdeptree &> /dev/null; then
    echo "Dependency tree:"
    pipdeptree --warn silence
else
    echo "Installing pipdeptree..."
    pip install pipdeptree
    echo "Dependency tree:"
    pipdeptree --warn silence
fi

# Security check
echo ""
echo "4. Running security check..."
if command -v safety &> /dev/null; then
    safety check || echo "⚠️  Security issues found - review recommended"
else
    echo "Installing safety..."
    pip install safety
    safety check || echo "⚠️  Security issues found - review recommended"
fi

echo ""
echo "✅ Dependency check complete!"
echo "=================================================="
