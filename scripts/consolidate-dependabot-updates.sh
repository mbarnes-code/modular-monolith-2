#!/bin/bash

# Consolidate Dependabot Updates Script
# Extracts dependency updates from all Dependabot branches and applies them with PNPM

set -e

echo "🔄 Consolidating Dependabot dependency updates..."

# Create consolidated update branch
git checkout -b consolidated-dependabot-updates-$(date +%Y%m%d)

echo "📦 JavaScript/Node.js Dependencies:"

# Extract JavaScript dependency updates
declare -A js_updates
js_updates[eslint]="9.39.1"
js_updates[eslint-config-next]="16.0.1" 
js_updates[@nx/workspace]="22.0.2"
js_updates[@nx/js]="22.0.2"
js_updates[@nx/react]="22.0.2"
js_updates[@nx/next]="22.0.2"
js_updates[@nx/node]="22.0.2"
js_updates[@nx/express]="22.0.2"
js_updates[@nx/eslint]="22.0.2"
js_updates[@types/node]="24.10.0"

# Apply JavaScript updates
for package in "${!js_updates[@]}"; do
    version="${js_updates[$package]}"
    echo "  ⬆️  $package → $version"
    pnpm update "$package@$version" 2>/dev/null || echo "    ⚠️  Could not update $package (may not be installed)"
done

echo ""
echo "🐍 Python Dependencies:"

# Python dependency updates (extract from Dependabot branches)
declare -A python_updates
python_updates[fastapi]="0.121.1"
python_updates[pydantic]="2.12.4"
python_updates[black]="25.11.0"
python_updates[mypy]="1.18.2"
python_updates[redis]="7.0.1"

# Apply Python updates to relevant services
for service in "jane-orchestrator" "cyber-llm-server" "mtg-llm-server" "code-llm-server"; do
    if [ -f "apps/$service/requirements.txt" ]; then
        echo "  📁 Updating apps/$service..."
        cd "apps/$service"
        
        for package in "${!python_updates[@]}"; do
            version="${python_updates[$package]}"
            if grep -q "^$package" requirements.txt 2>/dev/null; then
                echo "    ⬆️  $package → $version"
                sed -i.bak "s/^$package[>=<].*/$package==$version/" requirements.txt
            fi
        done
        
        cd - > /dev/null
    fi
done

echo ""
echo "✅ Dependency updates applied!"
echo "📝 Next steps:"
echo "   1. Review changes: git diff"
echo "   2. Test the updates: pnpm install && make test"
echo "   3. Commit changes: git commit -am 'chore: consolidate dependabot updates'"
echo "   4. Push branch: git push origin consolidated-dependabot-updates-$(date +%Y%m%d)"

echo ""
echo "🗑️  After testing, you can delete Dependabot branches:"
echo "   git push --delete origin \$(git branch -r | grep 'dependabot' | tr -d ' ' | sed 's/origin\///')"