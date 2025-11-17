#!/bin/bash

# Generate Mermaid Diagrams Script
# Usage: ./generate-diagrams.sh [filename.mmd] or ./generate-diagrams.sh (for all)

set -e

echo "🎨 Mermaid Diagram Generator"
echo "============================"

if [ $# -eq 1 ]; then
    # Generate specific diagram
    input_file="$1"
    if [ ! -f "$input_file" ]; then
        echo "❌ File $input_file not found!"
        exit 1
    fi
    
    base_name="${input_file%.*}"
    echo "📊 Generating diagrams for: $input_file"
    
    npx mmdc -i "$input_file" -o "${base_name}.png"
    npx mmdc -i "$input_file" -o "${base_name}.svg"
    
    echo "✅ Generated:"
    echo "   - ${base_name}.png"
    echo "   - ${base_name}.svg"
else
    # Generate all .mmd files
    echo "📊 Generating all Mermaid diagrams..."
    
    for mmd_file in *.mmd; do
        if [ -f "$mmd_file" ]; then
            base_name="${mmd_file%.*}"
            echo "  Processing: $mmd_file"
            
            npx mmdc -i "$mmd_file" -o "${base_name}.png"
            npx mmdc -i "$mmd_file" -o "${base_name}.svg"
        fi
    done
    
    echo ""
    echo "✅ All diagrams generated!"
fi

echo ""
echo "📋 Available diagram files:"
ls -la *.png *.svg *.mmd 2>/dev/null | head -20

echo ""
echo "💡 Tips:"
echo "   - View PNG files: code <filename>.png"
echo "   - Edit source: code <filename>.mmd"
echo "   - Regenerate: ./generate-diagrams.sh <filename>.mmd"