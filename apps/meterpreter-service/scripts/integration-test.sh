#!/bin/bash
# Integration test script for Meterpreter payloads
set -e

echo "🔍 Running Meterpreter Integration Tests"

# Check if outputs exist
if [ ! -d "output" ]; then
    echo "❌ No output directory found. Run 'nx build meterpreter-service' first."
    exit 1
fi

# Basic file validation
echo "📁 Checking build outputs..."
if ls output/*.bin >/dev/null 2>&1; then
    echo "✅ Binary payloads found"
    ls -la output/*.bin
else
    echo "⚠️  No .bin files found in output/"
fi

if ls output/*.lso >/dev/null 2>&1; then
    echo "✅ Extension libraries found"
    ls -la output/*.lso
else
    echo "⚠️  No .lso files found in output/"
fi

# File type analysis
echo "🔬 Analyzing file types..."
for file in output/*; do
    if [ -f "$file" ]; then
        echo "📄 $(basename "$file"): $(file "$file")"
    fi
done

# Basic security checks
echo "🛡️  Running basic security validation..."
for file in output/*.bin output/*.lso; do
    if [ -f "$file" ]; then
        size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file")
        echo "📏 $(basename "$file"): ${size} bytes"
        
        # Check for obvious issues
        if [ "$size" -eq 0 ]; then
            echo "❌ $(basename "$file") is empty!"
        elif [ "$size" -lt 1000 ]; then
            echo "⚠️  $(basename "$file") is suspiciously small (${size} bytes)"
        else
            echo "✅ $(basename "$file") size looks reasonable"
        fi
    fi
done

echo "✅ Integration tests completed"