#!/bin/bash
set -e

echo "Patching browser-use to force headless mode..."
python patch_browser_use.py

echo "Starting Xvfb..."
Xvfb :99 -screen 0 1920x1080x24 &
XVFB_PID=$!

# Wait for Xvfb to start
sleep 2

export DISPLAY=:99

echo "Xvfb started on DISPLAY=$DISPLAY"
echo "Running environment variable test..."
python test_env.py

echo "Starting application..."
python start.py

# Cleanup on exit
trap "kill $XVFB_PID" EXIT
