#!/bin/bash
# Ensure proper permissions for X11 socket
rm -rf /tmp/.X11-unix && mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

# Start Xvfb on a different display if needed
DISPLAY_NUM=99
Xvfb :${DISPLAY_NUM} -screen 0 1024x768x16 -ac -nolisten tcp +extension GLX +render -noreset 2>&1 &
XVFB_PID=$!

# Wait for Xvfb
for i in {1..10}; do
  if xdpyinfo -display :${DISPLAY_NUM} >/dev/null 2>&1; then
    break
  fi
  sleep 0.5
  if [[ $i -eq 10 ]]; then
    echo "Xvfb failed to start after 10 attempts" >&2
    exit 1
  fi
done

export DISPLAY=:${DISPLAY_NUM}

# Run your application
exec python3 src/main.py

# Cleanup
kill ${XVFB_PID}