#!/bin/bash

set -e

echo "🧹 Removing old virtual environment..."
rm -rf .venv

echo "🐍 Creating new virtual environment..."
uv venv

echo "📦 Setting UV_FORCE_SYSTEM_PYTHON=1 to prevent reinstall issues"
export UV_FORCE_SYSTEM_PYTHON=1

echo "🔧 Installing project dependencies and dev tools..."
uv sync --group dev

echo "⚡ Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "🚀 Setup complete! You can now run:"
echo ""
echo "    uv run app"
echo ""