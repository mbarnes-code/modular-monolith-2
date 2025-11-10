#!/bin/bash
# Start Constitutional Performance Monitoring
# T137 - Continuous monitoring daemon

echo "🎯 Starting Constitutional Performance Monitoring"
echo "Monitoring constitutional compliance thresholds..."

# Check if Python environment is ready
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is required"
    exit 1
fi

# Load monitoring configuration
if [ -f monitoring.env ]; then
    source monitoring.env
    echo "Loaded monitoring configuration"
else
    echo "Using default monitoring configuration"
fi

# Create monitoring data directory
mkdir -p monitoring_data
echo "Created monitoring data directory"

# Start the continuous monitor
echo "Starting performance monitor..."
python3 src/services/performance/continuous_monitor.py &
MONITOR_PID=$!

echo "Performance monitor started with PID: $MONITOR_PID"
echo "Monitoring endpoints for constitutional compliance:"
echo "  - Security Domain: <1s response time"
echo "  - Productivity Domain: <2s response time"  
echo "  - MTG Domain: <3s response time"
echo "  - Infrastructure Domain: <5s response time"
echo "  - UI Response: <200ms (executive function support)"
echo ""
echo "Press Ctrl+C to stop monitoring"

# Handle graceful shutdown
cleanup() {
    echo ""
    echo "🛑 Stopping performance monitor..."
    kill $MONITOR_PID 2>/dev/null
    wait $MONITOR_PID 2>/dev/null
    echo "Performance monitor stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for monitor process
wait $MONITOR_PID