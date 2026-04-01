# Deploy Predictive Dashboard to Streamlit Cloud

## Quick Steps (2 minutes):

1. **Go to:** https://streamlit.io/cloud

2. **Click "New app"**

3. **Fill in:**
   - **Repository:** `sscully2525/portfolio`
   - **Branch:** `main`
   - **Main file path:** `projects/predictive-dashboard/app.py`
   - **App URL:** `predictive-dashboard` (or whatever you want)

4. **Click "Deploy"**

5. **Wait 2-3 minutes** for it to build

6. **Your app will be at:**
   ```
   https://predictive-dashboard-sscully2525.streamlit.app
   ```

## That's it!

## Optional: Prophet Installation

If you want Prophet forecasting, you may need to add this to requirements:
```
prophet>=1.1.0
```

But the app works fine without it (falls back to other models).
