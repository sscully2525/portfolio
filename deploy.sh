#!/bin/bash

echo "🚀 GitHub Pages Deployment Helper"
echo "=================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Installing..."
    sudo apt update && sudo apt install -y git
fi

# Get GitHub username
echo "Enter your GitHub username:"
read GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Username cannot be empty"
    exit 1
fi

# Get repo name
echo "Enter repository name (default: portfolio):"
read REPO_NAME
REPO_NAME=${REPO_NAME:-portfolio}

echo ""
echo "📋 Summary:"
echo "  GitHub Username: $GITHUB_USERNAME"
echo "  Repository: $REPO_NAME"
echo "  URL will be: https://$GITHUB_USERNAME.github.io/$REPO_NAME"
echo ""
echo "Continue? (y/n)"
read CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "❌ Cancelled"
    exit 1
fi

# Navigate to project directory
cd /home/srscully/.openclaw/workspace/seanscully-website

# Initialize git if not already
git init

# Configure git (if not already set)
git config user.email "sean@example.com" 2>/dev/null || true
git config user.name "Sean Scully" 2>/dev/null || true

# Add all files
git add .

# Commit
git commit -m "Initial portfolio deployment" || echo "Already committed"

# Add remote
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo ""
echo "📤 Pushing to GitHub..."
echo "You may be asked to authenticate with GitHub"
echo ""

# Push
git branch -M main
git push -u origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "📝 Next steps:"
echo "   1. Go to: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "   2. Click Settings → Pages"
echo "   3. Under Source, select 'Deploy from a branch'"
echo "   4. Select 'main' branch and '/' folder"
echo "   5. Click Save"
echo ""
echo "🌐 Your portfolio will be live at:"
echo "   https://$GITHUB_USERNAME.github.io/$REPO_NAME"
echo ""
echo "⏳ Deployment takes 1-5 minutes"
echo ""
