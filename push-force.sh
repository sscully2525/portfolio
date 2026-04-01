#!/bin/bash

echo "🔍 Checking git status..."

cd /home/srscully/.openclaw/workspace/seanscully-website

# Check status
git status

echo ""
echo "📤 Pushing changes..."

# Add all changes
git add -A

# Commit with message
git commit -m "Updated portfolio with correct Streamlit and Hugging Face links"

# Push to GitHub
git push origin main

echo ""
echo "✅ Push complete!"
echo ""
echo "Check your repo: https://github.com/sscully2525/portfolio"
