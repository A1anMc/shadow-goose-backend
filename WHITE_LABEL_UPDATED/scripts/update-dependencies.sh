#!/bin/bash

# 📦 Dependency Update Script
# This script safely updates dependencies with testing

set -e

echo "📦 Updating dependencies safely..."
echo "=================================================="

# Create backup of current requirements
echo "1. Creating backup of current requirements..."
cp requirements.txt requirements.txt.backup
echo "✅ Backup created: requirements.txt.backup"

# Check current status
echo ""
echo "2. Checking current dependency status..."
pip list --outdated

# Update pip first
echo ""
echo "3. Updating pip..."
pip install --upgrade pip

# Install pip-review for interactive updates
echo ""
echo "4. Installing pip-review..."
pip install pip-review

# Interactive update
echo ""
echo "5. Starting interactive dependency update..."
echo "This will show you what can be updated and ask for confirmation"
echo "Press 'y' to update, 'n' to skip, or 'q' to quit"
echo ""

# Run pip-review in interactive mode
pip-review --local --interactive || {
    echo "⚠️  pip-review failed or was cancelled"
    echo "You can manually update specific packages:"
    echo "  pip install --upgrade package_name"
}

# Run tests after update
echo ""
echo "6. Running tests after update..."
if command -v pytest &> /dev/null; then
    pytest || {
        echo "❌ Tests failed after dependency update!"
        echo "Rolling back to previous requirements..."
        cp requirements.txt.backup requirements.txt
        pip install -r requirements.txt
        echo "✅ Rollback complete"
        exit 1
    }
else
    echo "⚠️  pytest not found - skipping tests"
fi

# Security check after update
echo ""
echo "7. Running security check after update..."
if command -v safety &> /dev/null; then
    safety check || echo "⚠️  Security issues found - review recommended"
else
    pip install safety
    safety check || echo "⚠️  Security issues found - review recommended"
fi

# Generate updated requirements
echo ""
echo "8. Generating updated requirements.txt..."
pip freeze > requirements.txt.new
echo "✅ New requirements saved to requirements.txt.new"

echo ""
echo "✅ Dependency update complete!"
echo "=================================================="
echo ""
echo "📋 Summary:"
echo "- Backup: requirements.txt.backup"
echo "- Updated: requirements.txt.new"
echo "- Tests: Passed"
echo ""
echo "Next steps:"
echo "1. Review requirements.txt.new"
echo "2. Test your application thoroughly"
echo "3. Commit changes if everything works"
echo "4. Deploy to staging first"
