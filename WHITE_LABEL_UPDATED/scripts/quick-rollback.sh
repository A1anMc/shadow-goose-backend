#!/bin/bash

# Quick Rollback Script for Direct Deployment
# Allows fast rollback to previous version if issues occur

set -e

echo "🔄 Quick Rollback Script"
echo "========================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_error "Not in a git repository"
    exit 1
fi

# Check current status
echo "📊 Current Status:"
echo "Branch: $(git branch --show-current)"
echo "Last commit: $(git log -1 --oneline)"
echo ""

# Show recent commits for rollback options
echo "📋 Recent commits (last 5):"
git log --oneline -5
echo ""

# Ask for confirmation
read -p "🤔 Do you want to rollback to the previous commit? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Rollback cancelled"
    exit 0
fi

# Perform rollback
echo "🔄 Performing rollback..."

# Create a revert commit
if git revert HEAD --no-edit; then
    print_status "Rollback commit created successfully"
else
    print_error "Failed to create rollback commit"
    exit 1
fi

# Push the rollback
echo "📤 Pushing rollback to production..."
if git push origin main; then
    print_status "Rollback pushed successfully"
    echo ""
    echo "🎉 Rollback completed!"
    echo "The previous version is now being deployed to production."
    echo ""
    echo "📋 What happened:"
    echo "- Created a revert commit for the last change"
    echo "- Pushed to main branch"
    echo "- Triggered automatic deployment to production"
    echo ""
    echo "⏳ Deployment should complete in 5-10 minutes"
    echo "🔍 Monitor the deployment logs for confirmation"
else
    print_error "Failed to push rollback"
    exit 1
fi

echo ""
echo "📞 Next steps:"
echo "1. Monitor deployment logs"
echo "2. Verify the rollback worked"
echo "3. Investigate the original issue"
echo "4. Fix the issue in a new commit"
echo ""
echo "🔧 To fix and redeploy:"
echo "git revert HEAD  # Undo the rollback"
echo "git push origin main  # Deploy the fix"
