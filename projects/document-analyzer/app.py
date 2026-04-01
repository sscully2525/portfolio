import streamlit as st
import PyPDF2
import docx
import pytesseract
from PIL import Image
import io
import re
from collections import Counter
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Smart Document Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        text-align: center;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b, #334155);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #475569;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #6366f1;
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
    }
    .result-box {
        background: #1e293b;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #6366f1;
        margin: 1rem 0;
    }
    .entity-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .entity-person { background: #dbeafe; color: #1e40af; }
    .entity-org { background: #fce7f3; color: #9d174d; }
    .entity-location { background: #d1fae5; color: #065f46; }
    .entity-date { background: #fef3c7; color: #92400e; }
    .entity-email { background: #e0e7ff; color: #3730a3; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📄 Smart Document Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Extract insights from documents using AI-powered NLP and OCR</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Analysis Options")
    
    st.subheader("Select Features")
    extract_entities = st.checkbox("🔍 Named Entity Recognition", value=True)
    sentiment_analysis = st.checkbox("😊 Sentiment Analysis", value=True)
    generate_summary = st.checkbox("📝 Generate Summary", value=True)
    word_cloud = st.checkbox("☁️ Word Cloud", value=True)
    keyword_extraction = st.checkbox("🔑 Keyword Extraction", value=True)
    
    st.markdown("---")
    
    st.subheader("Summary Length")
    summary_length = st.slider("Sentences", 1, 10, 3)
    
    st.markdown("---")
    
    st.info("💡 **Tip:** Upload PDF, Word, or image files to get started!")

# File upload
st.subheader("📤 Upload Document")
uploaded_file = st.file_uploader(
    "Choose a file",
    type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'],
    help="Supported formats: PDF, Word, Text, Images"
)

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    """Extract text from Word document"""
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_image(file):
    """Extract text from image using OCR"""
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text

def simple_summarize(text, num_sentences=3):
    """Simple extractive summarization"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(sentences) <= num_sentences:
        return text
    
    # Score sentences by word frequency
    word_freq = Counter(re.findall(r'\w+', text.lower()))
    sentence_scores = []
    
    for sentence in sentences:
        score = sum(word_freq[word.lower()] for word in re.findall(r'\w+', sentence))
        sentence_scores.append((score, sentence))
    
    # Get top sentences
    sentence_scores.sort(reverse=True)
    top_sentences = [s[1] for s in sentence_scores[:num_sentences]]
    
    # Reorder by original position
    ordered = sorted(top_sentences, key=lambda s: text.find(s))
    return '. '.join(ordered) + '.'

def extract_entities_simple(text):
    """Simple entity extraction using regex patterns"""
    entities = {
        'Person': [],
        'Organization': [],
        'Location': [],
        'Date': [],
        'Email': []
    }
    
    # Email pattern
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    entities['Email'] = list(set(emails))
    
    # Date patterns
    date_patterns = [
        r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
        r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
    ]
    for pattern in date_patterns:
        dates = re.findall(pattern, text, re.IGNORECASE)
        entities['Date'].extend(dates)
    entities['Date'] = list(set(entities['Date']))
    
    # Capitalized words (potential names/orgs)
    words = re.findall(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', text)
    entities['Person'] = list(set(words[:10]))  # Limit to first 10
    
    return entities

def analyze_sentiment_simple(text):
    """Simple sentiment analysis"""
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'best', 'happy', 'positive', 'success', 'win', 'improve', 'better', 'awesome']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'sad', 'negative', 'fail', 'loss', 'problem', 'issue', 'wrong', 'error', 'difficult', 'poor']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    total = positive_count + negative_count
    if total == 0:
        return {'sentiment': 'Neutral', 'score': 0.5, 'positive': 0, 'negative': 0}
    
    score = positive_count / total
    if score > 0.6:
        sentiment = 'Positive'
    elif score < 0.4:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    return {
        'sentiment': sentiment,
        'score': score,
        'positive': positive_count,
        'negative': negative_count
    }

def extract_keywords(text, num_keywords=10):
    """Extract keywords using frequency analysis"""
    # Common stop words
    stop_words = set(['the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'under', 'and', 'but', 'or', 'yet', 'so', 'if', 'because', 'although', 'though', 'while', 'where', 'when', 'that', 'which', 'who', 'whom', 'whose', 'what', 'this', 'these', 'those', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing'])
    
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    words = [w for w in words if w not in stop_words]
    
    word_freq = Counter(words)
    return word_freq.most_common(num_keywords)

# Main processing
if uploaded_file is not None:
    st.success(f"✅ Uploaded: **{uploaded_file.name}**")
    
    # Extract text based on file type
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    with st.spinner("🔍 Extracting text from document..."):
        try:
            if file_type == 'pdf':
                text = extract_text_from_pdf(uploaded_file)
            elif file_type == 'docx':
                text = extract_text_from_docx(uploaded_file)
            elif file_type in ['png', 'jpg', 'jpeg']:
                text = extract_text_from_image(uploaded_file)
            else:
                text = uploaded_file.getvalue().decode('utf-8')
            
            if not text.strip():
                st.error("❌ Could not extract text from the document. Please try another file.")
            else:
                # Document Statistics
                col1, col2, col3, col4 = st.columns(4)
                
                word_count = len(text.split())
                char_count = len(text)
                sentence_count = len(re.split(r'[.!?]+', text))
                paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
                
                with col1:
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">{word_count:,}</div>
                        <div class="metric-label">Words</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">{char_count:,}</div>
                        <div class="metric-label">Characters</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">{sentence_count:,}</div>
                        <div class="metric-label">Sentences</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">{paragraph_count:,}</div>
                        <div class="metric-label">Paragraphs</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Create tabs for different analyses
                tabs = []
                if generate_summary:
                    tabs.append("Summary")
                if extract_entities:
                    tabs.append("Entities")
                if sentiment_analysis:
                    tabs.append("Sentiment")
                if keyword_extraction:
                    tabs.append("Keywords")
                if word_cloud:
                    tabs.append("Word Cloud")
                tabs.append("Full Text")
                
                if len(tabs) > 1:
                    active_tabs = st.tabs(tabs)
                    tab_idx = 0
                    
                    # Summary Tab
                    if generate_summary:
                        with active_tabs[tab_idx]:
                            st.subheader("📝 Document Summary")
                            summary = simple_summarize(text, summary_length)
                            st.markdown(f'<div class="result-box">{summary}</div>', unsafe_allow_html=True)
                            
                            with st.expander("View Full Text"):
                                st.text_area("", text, height=300)
                        tab_idx += 1
                    
                    # Entities Tab
                    if extract_entities:
                        with active_tabs[tab_idx]:
                            st.subheader("🔍 Named Entities")
                            entities = extract_entities_simple(text)
                            
                            for entity_type, items in entities.items():
                                if items:
                                    st.write(f"**{entity_type}:**")
                                    entity_class = entity_type.lower()
                                    if entity_class == 'person':
                                        css_class = 'entity-person'
                                    elif entity_class == 'organization':
                                        css_class = 'entity-org'
                                    elif entity_class == 'location':
                                        css_class = 'entity-location'
                                    elif entity_class == 'date':
                                        css_class = 'entity-date'
                                    elif entity_class == 'email':
                                        css_class = 'entity-email'
                                    else:
                                        css_class = 'entity-person'
                                    
                                    entity_html = ' '.join([f'<span class="entity-tag {css_class}">{item}</span>' for item in items[:15]])
                                    st.markdown(entity_html, unsafe_allow_html=True)
                                    st.write("")
                        tab_idx += 1
                    
                    # Sentiment Tab
                    if sentiment_analysis:
                        with active_tabs[tab_idx]:
                            st.subheader("😊 Sentiment Analysis")
                            sentiment = analyze_sentiment_simple(text)
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Sentiment gauge
                                fig = go.Figure(go.Indicator(
                                    mode = "gauge+number",
                                    value = sentiment['score'] * 100,
                                    domain = {'x': [0, 1], 'y': [0, 1]},
                                    title = {'text': "Sentiment Score"},
                                    gauge = {
                                        'axis': {'range': [0, 100]},
                                        'bar': {'color': "#6366f1"},
                                        'steps': [
                                            {'range': [0, 40], 'color': "#fecaca"},
                                            {'range': [40, 60], 'color': "#fef3c7"},
                                            {'range': [60, 100], 'color': "#bbf7d0"}
                                        ],
                                        'threshold': {
                                            'line': {'color': "red", 'width': 4},
                                            'thickness': 0.75,
                                            'value': 50
                                        }
                                    }
                                ))
                                fig.update_layout(height=300)
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                st.markdown(f"### Overall: **{sentiment['sentiment']}**")
                                st.write(f"**Positive indicators:** {sentiment['positive']}")
                                st.write(f"**Negative indicators:** {sentiment['negative']}")
                                
                                # Bar chart
                                sentiment_data = pd.DataFrame({
                                    'Sentiment': ['Positive', 'Negative'],
                                    'Count': [sentiment['positive'], sentiment['negative']]
                                })
                                fig = px.bar(sentiment_data, x='Sentiment', y='Count', 
                                            color='Sentiment', color_discrete_map={
                                                'Positive': '#10b981',
                                                'Negative': '#ef4444'
                                            })
                                fig.update_layout(showlegend=False, height=200)
                                st.plotly_chart(fig, use_container_width=True)
                        tab_idx += 1
                    
                    # Keywords Tab
                    if keyword_extraction:
                        with active_tabs[tab_idx]:
                            st.subheader("🔑 Top Keywords")
                            keywords = extract_keywords(text, 15)
                            
                            if keywords:
                                keyword_df = pd.DataFrame(keywords, columns=['Keyword', 'Frequency'])
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    fig = px.bar(keyword_df, x='Frequency', y='Keyword', 
                                                orientation='h', color='Frequency',
                                                color_continuous_scale='Viridis')
                                    fig.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
                                    st.plotly_chart(fig, use_container_width=True)
                                
                                with col2:
                                    st.dataframe(keyword_df, use_container_width=True, hide_index=True)
                        tab_idx += 1
                    
                    # Word Cloud Tab
                    if word_cloud:
                        with active_tabs[tab_idx]:
                            st.subheader("☁️ Word Cloud")
                            
                            # Generate word cloud
                            stopwords = set(['the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being'])
                            wordcloud = WordCloud(
                                width=800, 
                                height=400, 
                                background_color='#1e293b',
                                colormap='viridis',
                                stopwords=stopwords,
                                max_words=100
                            ).generate(text)
                            
                            fig, ax = plt.subplots(figsize=(12, 6))
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            ax.set_facecolor('#1e293b')
                            fig.patch.set_facecolor('#1e293b')
                            st.pyplot(fig)
                        tab_idx += 1
                    
                    # Full Text Tab
                    with active_tabs[tab_idx]:
                        st.subheader("📄 Full Document Text")
                        st.text_area("", text, height=500)
                
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")
            st.info("💡 Try uploading a different file format or check if the file is corrupted.")

else:
    # Show sample/demo section when no file uploaded
    st.info("👆 Upload a document to get started!")
    
    st.markdown("### 🎯 Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📄 Document Support**
        - PDF files
        - Word documents (.docx)
        - Text files (.txt)
        - Images (OCR) - PNG, JPG
        """)
    
    with col2:
        st.markdown("""
        **🤖 AI Analysis**
        - Named Entity Recognition
        - Sentiment Analysis
        - Keyword Extraction
        - Automatic Summarization
        """)
    
    with col3:
        st.markdown("""
        **📊 Visualizations**
        - Interactive charts
        - Word clouds
        - Sentiment gauges
        - Entity highlighting
        """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Sample Use Cases")
    
    use_cases = [
        ("📑 Resume Analysis", "Extract skills, experience, and contact information from resumes automatically"),
        ("📰 News Summarization", "Get quick summaries of long articles with sentiment and key entities"),
        ("📄 Contract Review", "Identify key dates, parties, and terms in legal documents"),
        ("🖼️ Image Text Extraction", "Convert scanned documents and images to editable text")
    ]
    
    for title, desc in use_cases:
        with st.expander(title):
            st.write(desc)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6b7280;'>Built with ❤️ using Streamlit | Smart Document Analyzer v1.0</p>", unsafe_allow_html=True)
