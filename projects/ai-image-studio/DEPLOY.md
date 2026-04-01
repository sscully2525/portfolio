# Deploy AI Image Studio to Hugging Face Spaces

## Quick Steps (3 minutes):

### Option 1: Git Push (Recommended)

1. **Create a Space:**
   - Go to: https://huggingface.co/spaces
   - Click "Create new Space"
   - **Space name:** `ai-image-studio`
   - **License:** Apache 2.0
   - **Space SDK:** Gradio
   - **Public:** Yes
   - Click "Create Space"

2. **Get your Space URL:**
   It will be: `https://huggingface.co/spaces/sscully2525/ai-image-studio`

3. **Clone and push (run these commands):**
   ```bash
   cd /tmp
   git clone https://huggingface.co/spaces/sscully2525/ai-image-studio
   cd ai-image-studio
   
   # Copy your files
   cp /home/srscully/.openclaw/workspace/seanscully-website/projects/ai-image-studio/* .
   
   # Push
   git add .
   git commit -m "Initial commit"
   git push
   ```

4. **Wait 2-3 minutes** for it to build

5. **Your app will be at:**
   ```
   https://sscully2525-ai-image-studio.hf.space
   ```

### Option 2: Direct Upload

1. Create the Space (same as above)
2. Click "Files" tab
3. Click "Upload files"
4. Upload `app.py` and `requirements.txt`
5. It will auto-deploy!

## That's it!

Hugging Face Spaces is free for public projects.
