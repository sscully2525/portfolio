#!/bin/bash

# Complete Portfolio Deployment Script
# This script sets up everything for deployment

echo "🚀 Complete Portfolio Setup & Deployment"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get user info
echo -e "${BLUE}Step 1: GitHub Configuration${NC}"
echo "Enter your GitHub username:"
read GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Username cannot be empty"
    exit 1
fi

echo "Enter your email (for git):"
read USER_EMAIL

if [ -z "$USER_EMAIL" ]; then
    USER_EMAIL="sean@example.com"
fi

echo ""
echo -e "${BLUE}Step 2: Setting up Git...${NC}"

# Install git if needed
if ! command -v git &> /dev/null; then
    echo "Installing Git..."
    sudo apt update -qq && sudo apt install -y -qq git
fi

# Configure git
git config --global user.email "$USER_EMAIL"
git config --global user.name "Sean Scully"

echo -e "${GREEN}✓ Git configured${NC}"

# Navigate to project
cd /home/srscully/.openclaw/workspace/seanscully-website

echo ""
echo -e "${BLUE}Step 3: Preparing files...${NC}"

# Create a .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
.env
.venv
venv/
ENV/
.DS_Store
EOF

echo -e "${GREEN}✓ Files prepared${NC}"

echo ""
echo -e "${BLUE}Step 4: Creating GitHub repository...${NC}"
echo ""
echo -e "${YELLOW}IMPORTANT: Create a repository on GitHub first!${NC}"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: portfolio"
echo "3. Make it PUBLIC"
echo "4. Click 'Create repository'"
echo ""
echo "Press ENTER when you've created the repo..."
read

echo ""
echo -e "${BLUE}Step 5: Pushing to GitHub...${NC}"

# Initialize and push
git init
git add .
git commit -m "Initial portfolio commit - AI/ML projects included" || true
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$GITHUB_USERNAME/portfolio.git"

echo ""
echo -e "${YELLOW}Pushing code... You may need to authenticate${NC}"
git push -u origin main

echo ""
echo -e "${GREEN}✓ Code pushed to GitHub!${NC}"

echo ""
echo -e "${BLUE}Step 6: Creating deployment instructions...${NC}"

cat > DEPLOY_NEXT_STEPS.txt << EOF
🎉 YOUR PORTFOLIO IS READY!
===========================

✅ COMPLETED:
   - Portfolio website created
   - 3 AI/ML projects built
   - Code pushed to GitHub

🌐 TO MAKE IT LIVE:

1. Enable GitHub Pages:
   - Go to: https://github.com/$GITHUB_USERNAME/portfolio/settings/pages
   - Under "Source", select "Deploy from a branch"
   - Select "main" branch and "/ (root)" folder
   - Click "Save"
   - Wait 1-5 minutes

2. Your portfolio will be at:
   https://$GITHUB_USERNAME.github.io/portfolio

🐍 TO DEPLOY PYTHON PROJECTS:

Document Analyzer & Predictive Dashboard (Streamlit):
   - Go to: https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select: $GITHUB_USERNAME/portfolio
   - File path: projects/document-analyzer/app.py
   - Deploy!
   - Repeat for predictive-dashboard

AI Image Studio (Hugging Face):
   - Go to: https://huggingface.co/spaces
   - Click "Create new Space"
   - Select Gradio SDK
   - Upload projects/ai-image-studio/
   - Deploy!

📱 TO ADD YOUR CONTENT:

1. Add your photo:
   - Replace the placeholder in index.html
   - Or add to assets/ folder

2. Add your resume:
   - Put your PDF as resume.pdf in the root

3. Update links:
   - GitHub: https://github.com/$GITHUB_USERNAME
   - LinkedIn: Edit in index.html
   - Email: Edit in index.html

🔄 TO UPDATE LATER:

cd /home/srscully/.openclaw/workspace/seanscully-website
git add .
git commit -m "Your update message"
git push

🆘 NEED HELP?

- GitHub Pages: https://pages.github.com
- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- Check DEPLOY.md for detailed instructions

🎉 YOU'RE ALL SET!
EOF

cat DEPLOY_NEXT_STEPS.txt

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}🎉 SETUP COMPLETE!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Next steps saved to: DEPLOY_NEXT_STEPS.txt"
echo ""
echo -e "${YELLOW}Quick Summary:${NC}"
echo "  GitHub Repo: https://github.com/$GITHUB_USERNAME/portfolio"
echo "  Portfolio URL (after enabling Pages): https://$GITHUB_USERNAME.github.io/portfolio"
echo ""
echo -e "${BLUE}Run this to see next steps anytime:${NC}"
echo "  cat /home/srscully/.openclaw/workspace/seanscully-website/DEPLOY_NEXT_STEPS.txt"
echo ""
