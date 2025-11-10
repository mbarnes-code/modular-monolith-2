#!/bin/bash
echo "Testing Mealie Service endpoints..."

echo -n "Health check: "
curl -s http://localhost:9925/health | jq -r '.status // "ERROR"'

echo -n "Jane status: "
curl -s http://localhost:9925/api/jane/status | jq -r '.service // "ERROR"'

echo -n "API proxy test: "
curl -s http://localhost:9925/api/recipes | jq -r '.error // "ERROR"'

echo "Tests completed."