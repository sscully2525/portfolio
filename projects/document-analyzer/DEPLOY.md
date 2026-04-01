# Deploy Document Analyzer to Streamlit Cloud

## Quick Steps (2 minutes):

1. **Go to:** https://streamlit.io/cloud

2. **Click "New app"**

3. **Fill in:**
   - **Repository:** `sscully2525/portfolio`
   - **Branch:** `main`
   - **Main file path:** `projects/document-analyzer/app.py`
   - **App URL:** `document-analyzer` (or whatever you want)

4. **Click "Deploy"**

5. **Wait 2-3 minutes** for it to build

6. **Your app will be at:**
   ```
   https://document-analyzer-sscully2525.streamlit.app
   ```

## That's it!

Streamlit Cloud is free and handles everything automatically.

## Troubleshooting:

If it fails, check that `requirements.txt` has all dependencies:
```
streamlit>=1.28.0
PyPDF2>=3.0.0
python-docx>=0.8.11
pytesseract>=0.3.10
Pillow>=10.0.0
matplotlib>=3.7.0
plotly>=5.15.0
wordcloud>=1.9.0
pandas>=2.0.0
numpy>=1.24.0
```

Note: OCR (pytesseract) might need special setup on Streamlit Cloud.
