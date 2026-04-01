#!/bin/bash
cd /home/srscully/.openclaw/workspace/seanscully-website
git add .
git commit -m "Updated all Streamlit app links"
git push
echo "✅ Portfolio updated with correct links!"
echo ""
echo "🌐 Your apps:"
echo "  Document Analyzer: https://document-analyzer-sean-scully.streamlit.app"
echo "  Predictive Dashboard: https://predictive-dashboard-sean-scully.streamlit.app"
echo ""
echo "⏳ Wait 1-2 minutes for GitHub Pages to refresh"
