# 🚀 Deploy to GitHub Pages

This guide will help you deploy your portfolio to GitHub Pages for free hosting.

## 📋 Prerequisites

1. GitHub account (free)
2. Git installed on your Pi

## 🛠️ Step-by-Step Deployment

### Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Repository name: `portfolio` (or any name you prefer)
3. Make it **Public**
4. Don't initialize with README (we have one already)
5. Click **Create repository**

### Step 2: Initialize Git and Push

Open terminal on your Pi and run:

```bash
# Navigate to your project
cd /home/srscully/.openclaw/workspace/seanscully-website

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial portfolio commit"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/portfolio.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (tab at the top)
3. Scroll down to **Pages** (left sidebar)
4. Under "Source", select **Deploy from a branch**
5. Select **main** branch and **/ (root)** folder
6. Click **Save**

### Step 4: Wait for Deployment

- GitHub will build and deploy your site (takes 1-5 minutes)
- Refresh the Pages settings to see your URL
- It will be: `https://YOUR_USERNAME.github.io/portfolio`

## 🎉 Done!

Your portfolio is now live at:
```
https://YOUR_USERNAME.github.io/portfolio
```

## 🔄 Making Updates

Whenever you make changes:

```bash
cd /home/srscully/.openclaw/workspace/seanscully-website
git add .
git commit -m "Update description"
git push
```

GitHub Pages will automatically update!

## 📱 Custom Domain (Optional)

To use your own domain (e.g., seanscully.com):

1. Buy a domain from Namecheap, Cloudflare, etc.
2. In your repo, create a file called `CNAME` with your domain:
   ```
   seanscully.com
   ```
3. Add these DNS records at your domain registrar:
   - Type: A, Name: @, Value: 185.199.108.153
   - Type: A, Name: @, Value: 185.199.109.153
   - Type: A, Name: @, Value: 185.199.110.153
   - Type: A, Name: @, Value: 185.199.111.153
   - Type: CNAME, Name: www, Value: YOUR_USERNAME.github.io

4. In GitHub Pages settings, add your custom domain

## 🐍 Deploying Python Projects

The Python apps (Streamlit/Gradio) can't run on GitHub Pages (static hosting only).

### Option 1: Streamlit Cloud (Free)
For the Document Analyzer & Predictive Dashboard:

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"
4. Select your portfolio repo
5. Set file path to `projects/document-analyzer/app.py`
6. Deploy!
7. Repeat for predictive-dashboard

### Option 2: Hugging Face Spaces (Free)
For the AI Image Studio (Gradio):

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Select Gradio SDK
4. Upload your files or connect GitHub
5. Deploy!

### Option 3: Render/Heroku
For production deployment with custom domains.

## 📊 After Deployment Checklist

- [ ] Portfolio loads at your GitHub Pages URL
- [ ] All images load correctly
- [ ] Links work (GitHub, LinkedIn, email)
- [ ] Mobile responsive (test on phone)
- [ ] Add your actual photo
- [ ] Upload your real resume.pdf
- [ ] Deploy Python projects to Streamlit Cloud
- [ ] Update project links in portfolio to point to live demos
- [ ] Share the link on LinkedIn!

## 🆘 Troubleshooting

**Changes not showing?**
- Clear browser cache (Ctrl+Shift+R)
- Wait 5 minutes for GitHub to rebuild

**404 error?**
- Make sure index.html is in the root
- Check GitHub Pages source is set to main branch

**Images not loading?**
- Use relative paths: `./assets/image.jpg`
- Check file names match exactly (case-sensitive)

**CSS not applying?**
- Check styles.css is in the same folder as index.html
- Verify the link in HTML is correct

## 📞 Need Help?

- GitHub Pages docs: https://pages.github.com
- Streamlit Cloud docs: https://docs.streamlit.io/streamlit-community-cloud

---

**Your portfolio will be live in under 10 minutes! 🚀**
