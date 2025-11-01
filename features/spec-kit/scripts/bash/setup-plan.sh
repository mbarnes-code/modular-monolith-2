#!/usr/bin/env bash

set -e

# Parse command line arguments
JSON_MODE=false
ARGS=()

for arg in "$@"; do
    case "$arg" in
        --json) 
            JSON_MODE=true 
            ;;
        --help|-h) 
            echo "Usage: $0 [--json]"
            echo "  --json    Output results in JSON format"
            echo "  --help    Show this help message"
            exit 0 
            ;;
        *) 
            ARGS+=("$arg") 
            ;;
    esac
done

# Get script directory and load common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Get all paths and variables from common functions
eval $(get_feature_paths)

# Check if we're on a proper feature branch (only for git repos)
check_feature_branch "$CURRENT_BRANCH" "$HAS_GIT" || exit 1

# Ensure the feature directory exists
mkdir -p "$FEATURE_DIR"

# Detect project type from spec.md if it exists
PROJECT_TYPE="GREENFIELD"  # default
if [[ -f "$FEATURE_SPEC" ]]; then
    PROJECT_TYPE=$(grep "Selected Project Type" "$FEATURE_SPEC" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "GREENFIELD")
fi

# Copy plan template if it exists
TEMPLATE="$REPO_ROOT/templates/plan-template.md"
if [[ -f "$TEMPLATE" ]]; then
    cp "$TEMPLATE" "$IMPL_PLAN"
    
    # Replace project type placeholder in plan
    if command -v sed >/dev/null 2>&1; then
        sed -i.bak "s/\[GREENFIELD\/BROWNFIELD\]/$PROJECT_TYPE/g" "$IMPL_PLAN" && rm "$IMPL_PLAN.bak"
    fi
    
    echo "Copied plan template to $IMPL_PLAN (Project Type: $PROJECT_TYPE)"
else
    echo "Warning: Plan template not found at $TEMPLATE"
    # Create a basic plan file if template doesn't exist
    touch "$IMPL_PLAN"
fi

# Create brownfield-specific files if needed
if [ "$PROJECT_TYPE" = "BROWNFIELD" ]; then
    echo "Detected brownfield project - creating additional migration files..."
    
    # Create migration-strategy.md if it doesn't exist
    MIGRATION_STRATEGY="$FEATURE_DIR/migration-strategy.md"
    if [[ ! -f "$MIGRATION_STRATEGY" ]]; then
        MIGRATION_TEMPLATE="$REPO_ROOT/templates/migration-strategy-template.md"
        if [[ -f "$MIGRATION_TEMPLATE" ]]; then
            cp "$MIGRATION_TEMPLATE" "$MIGRATION_STRATEGY"
            echo "Created migration strategy file: $MIGRATION_STRATEGY"
        fi
    fi
    
    # TODO: Create other brownfield files when templates are available
    # legacy-analysis.md, data-mapping.md, etc.
fi

# Output results
if $JSON_MODE; then
    printf '{"FEATURE_SPEC":"%s","IMPL_PLAN":"%s","SPECS_DIR":"%s","BRANCH":"%s","HAS_GIT":"%s","PROJECT_TYPE":"%s"}\n' \
        "$FEATURE_SPEC" "$IMPL_PLAN" "$FEATURE_DIR" "$CURRENT_BRANCH" "$HAS_GIT" "$PROJECT_TYPE"
else
    echo "FEATURE_SPEC: $FEATURE_SPEC"
    echo "IMPL_PLAN: $IMPL_PLAN" 
    echo "SPECS_DIR: $FEATURE_DIR"
    echo "BRANCH: $CURRENT_BRANCH"
    echo "HAS_GIT: $HAS_GIT"
    echo "PROJECT_TYPE: $PROJECT_TYPE"
fi

