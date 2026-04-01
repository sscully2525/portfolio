#!/bin/bash
cd /home/srscully/.openclaw/workspace/seanscully-website
git add .
git commit -m "Fixed demo links to actual deployed URLs"
git push
echo "✅ Updated! Wait 1-2 minutes for GitHub Pages to refresh"
