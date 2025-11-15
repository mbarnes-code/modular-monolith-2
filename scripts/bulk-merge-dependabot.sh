#!/bin/bash

# Bulk merge Dependabot PRs using GitHub CLI
# Requires: gh cli tool installed and authenticated

echo "🔍 Finding Dependabot PRs..."

# List all open Dependabot PRs
dependabot_prs=$(gh pr list --author "app/dependabot" --json number,title --jq '.[].number')

if [ -z "$dependabot_prs" ]; then
    echo "❌ No open Dependabot PRs found"
    exit 0
fi

echo "📋 Found Dependabot PRs:"
gh pr list --author "app/dependabot" --json number,title --jq '.[] | "  #\(.number): \(.title)"'

echo ""
read -p "🤔 Merge all Dependabot PRs? (y/N): " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    echo "🚀 Merging Dependabot PRs..."
    
    for pr in $dependabot_prs; do
        echo "  ⬆️  Merging PR #$pr..."
        gh pr merge "$pr" --squash --auto || echo "    ⚠️  Failed to merge PR #$pr"
    done
    
    echo "✅ Bulk merge complete!"
else
    echo "❌ Bulk merge cancelled"
fi