#!/bin/bash

# Local development runner for Brian VEAU AI Agent using uv

echo "🚀 Starting Brian VEAU AI Agent locally with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Initialize project if needed
if [ ! -f "pyproject.toml" ]; then
    echo "❌ pyproject.toml not found!"
    exit 1
fi

# Install dependencies
echo "📚 Installing dependencies with uv..."
uv sync

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Creating .env from template..."
    cp .env.template .env
    echo "✏️  Please edit .env file with your API keys and run again"
    exit 1
fi

# Check if required files exist
required_files=("resume.pdf" "personal_info.txt")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if API keys are set
if [ -z "$OPENAI_API_KEY" ] || [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ API keys not set in .env file"
    echo "Please update .env with your actual API keys"
    exit 1
fi

echo "✅ Environment ready!"
echo "🌐 Starting application on http://localhost:8080"
echo "📋 Press Ctrl+C to stop"

# Run the application with uv
uv run python main.py