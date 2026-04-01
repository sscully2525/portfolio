#!/bin/bash

cd /home/srscully/.openclaw/workspace/seanscully-website

echo "🚀 Pushing updated portfolio..."

git add .
git commit -m "Updated with live demo links"
git push

echo "✅ Done!"
