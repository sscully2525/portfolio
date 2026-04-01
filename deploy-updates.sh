#!/bin/bash

echo "🚀 Deploying Portfolio Updates"
echo "==============================="
echo ""

cd /home/srscully/.openclaw/workspace/seanscully-website

echo "📤 Pushing to GitHub..."
git add .
git commit -m "Fixed demo links to actual deployed URLs" || echo "Nothing to commit"
git push

echo ""
echo "✅ Portfolio updated!"
echo ""
echo "🌐 Your portfolio will refresh at:"
echo "   https://sscully2525.github.io/portfolio"
echo ""
echo "⏳ Wait 1-2 minutes for changes to appear"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. Document Analyzer is LIVE at:"
echo "   https://portfolio-nsviw3iwaesykjuk6ewnhv.streamlit.app"
echo ""
echo "2. To deploy the other projects:"
echo ""
echo "   PREDICTIVE DASHBOARD (Streamlit):"
echo "   - Go to: https://streamlit.io/cloud"
echo "   - Click 'New app'"
echo "   - Repository: sscully2525/portfolio"
echo "   - File path: projects/predictive-dashboard/app.py"
echo "   - Set to PUBLIC and deploy"
echo ""
echo "   AI IMAGE STUDIO (Hugging Face):"
echo "   - Go to: https://huggingface.co/spaces/sscully2525/ai-image-studio"
echo "   - Click 'Files' tab"
echo "   - Upload: app.py and requirements.txt"
echo "   - Commit changes"
echo ""
echo "3. Once deployed, tell me the URLs and I'll update your portfolio!"
echo ""
