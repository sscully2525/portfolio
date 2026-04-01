# Sean Scully - Personal Portfolio & AI Projects

🎨 **A modern portfolio website showcasing AI/ML projects built with Python**

![Portfolio Preview](assets/preview.png)

## 🚀 Quick Start

### 1. Portfolio Website
The main portfolio is a static HTML/CSS/JS site. Simply open `index.html` in your browser:

```bash
cd seanscully-website
# Open index.html in your browser
# OR serve locally:
python -m http.server 8000
```

### 2. AI/ML Projects

Each project is a standalone Python application with its own dependencies.

#### Project 1: Smart Document Analyzer
```bash
cd projects/document-analyzer
pip install -r requirements.txt
streamlit run app.py
```

**Features:**
- PDF, Word, and image OCR support
- Named Entity Recognition
- Sentiment Analysis
- Automatic Summarization
- Word Cloud generation
- Interactive visualizations

#### Project 2: AI Image Studio
```bash
cd projects/ai-image-studio
pip install -r requirements.txt
python app.py
```

**Features:**
- Text-to-image generation (placeholder)
- Background removal
- Image enhancement (brightness, contrast, saturation)
- Filters & effects (grayscale, sepia, edge detection, etc.)
- Style transfer (oil painting, sketch, watercolor)
- Collage maker
- Watermarking

#### Project 3: Predictive Analytics Dashboard
```bash
cd projects/predictive-dashboard
pip install -r requirements.txt
streamlit run app.py
```

**Features:**
- Time series forecasting (Prophet, Linear, Polynomial, etc.)
- Confidence intervals
- Anomaly detection
- Trend analysis
- Seasonality decomposition
- Interactive charts

## 📁 Project Structure

```
seanscully-website/
├── index.html              # Main portfolio page
├── styles.css              # Styling
├── script.js               # Interactivity
├── resume.pdf              # Your resume (add your own)
├── assets/                 # Images and assets
└── projects/
    ├── document-analyzer/  # Project 1
    │   ├── app.py
    │   └── requirements.txt
    ├── ai-image-studio/    # Project 2
    │   ├── app.py
    │   └── requirements.txt
    └── predictive-dashboard/  # Project 3
        ├── app.py
        └── requirements.txt
```

## 🛠️ Tech Stack

### Portfolio Website
- HTML5, CSS3, JavaScript
- Modern dark theme with gradients
- Responsive design
- Smooth animations
- Intersection Observer API

### AI/ML Projects
- **Python** - Core language
- **Streamlit** - Web apps for data science
- **Gradio** - ML model demos
- **OpenCV** - Computer vision
- **PIL/Pillow** - Image processing
- **Plotly** - Interactive visualizations
- **Prophet** - Time series forecasting
- **scikit-learn** - Machine learning

## 🎯 Features for Recruiters

### Portfolio Highlights
✅ Clean, modern design with dark theme  
✅ Mobile responsive  
✅ Fast loading (static site)  
✅ Interactive code animation  
✅ Skills visualization  
✅ Project showcase with live demos  
✅ Contact form  
✅ Resume download  

### Project Demos
✅ **Document Analyzer** - Shows NLP, OCR, data viz skills  
✅ **AI Image Studio** - Shows computer vision, image processing  
✅ **Predictive Dashboard** - Shows forecasting, analytics, ML  

## 📝 Customization

### Add Your Photo
Replace the placeholder in the About section:
```html
<div class="placeholder-image">
    <!-- Add your image here -->
    <img src="your-photo.jpg" alt="Sean Scully">
</div>
```

### Update Contact Info
Edit the Contact section in `index.html`:
```html
<a href="mailto:your-email@example.com">your-email@example.com</a>
<a href="https://github.com/yourusername">github.com/yourusername</a>
<a href="https://linkedin.com/in/yourprofile">linkedin.com/in/yourprofile</a>
```

### Add Your Resume
Replace `resume.pdf` with your actual resume.

## 🚀 Deployment

### Portfolio Website
- **GitHub Pages**: Push to GitHub and enable Pages
- **Netlify**: Drag and drop the folder
- **Vercel**: Connect your GitHub repo
- **AWS S3**: Static website hosting

### Python Projects
Deploy to:
- **Streamlit Cloud**: For Streamlit apps
- **Hugging Face Spaces**: For Gradio apps
- **Heroku**: For full-stack deployment
- **AWS/GCP/Azure**: For production scaling

## 📄 License

MIT License - Feel free to use this template for your own portfolio!

## 🤝 Connect

- GitHub: [@seanscully](https://github.com/seanscully)
- LinkedIn: [linkedin.com/in/seanscully](https://linkedin.com/in/seanscully)
- Email: sean@example.com

---

Built with ❤️ by Sean Scully
