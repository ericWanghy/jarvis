#!/bin/bash

# Kill any existing processes on ports 3721 (Backend) and 1420 (Frontend)
lsof -ti:3721 | xargs kill -9 2>/dev/null
lsof -ti:1420 | xargs kill -9 2>/dev/null

echo "🚀 Starting Jarvis v5.6-proxy Dev Environment..."

# Get absolute path to the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$SCRIPT_DIR"

# Ensure Rust/Cargo is in PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Check if cargo exists
if ! command -v cargo &> /dev/null; then
    echo "❌ Error: Rust/Cargo is not installed or not in PATH."
    echo "Please install Rust: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi

# Start Backend
echo "🐍 Starting Backend (Port 3721)..."
cd "$ROOT_DIR/backend"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run backend in background
# Use absolute path to venv python to avoid system pollution
"$ROOT_DIR/backend/venv/bin/python" run.py > "$ROOT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo "Backend running (PID: $BACKEND_PID). Logs: backend.log"

# Start Frontend
echo "⚛️  Starting Frontend (Tauri)..."
cd "$ROOT_DIR/frontend"
npm run tauri dev

# Cleanup when frontend exits
echo "🛑 Shutting down..."
kill $BACKEND_PID
