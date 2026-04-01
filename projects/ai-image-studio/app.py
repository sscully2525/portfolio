import gradio as gr
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import cv2
import io
import base64
from datetime import datetime

# Page title and description
title = "🎨 AI Image Studio"
description = """
Transform your images with AI-powered tools. Generate images from text, remove backgrounds, 
apply style transfers, enhance resolution, and more!
"""

# Custom CSS for styling
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

.gradio-container {
    max-width: 1400px !important;
}

.header-text {
    text-align: center;
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.subheader-text {
    text-align: center;
    color: #94a3b8;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

.tool-card {
    background: linear-gradient(135deg, #1e293b, #334155);
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid #475569;
    transition: all 0.3s ease;
}

.tool-card:hover {
    border-color: #6366f1;
    transform: translateY(-2px);
}

.primary-button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}

.primary-button:hover {
    background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.image-preview {
    border-radius: 12px;
    border: 2px solid #475569;
    overflow: hidden;
}

.tabs {
    background: #1e293b !important;
    border-radius: 12px !important;
    border: 1px solid #475569 !important;
}

.tab-selected {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    color: white !important;
}

.input-label {
    color: #e2e8f0 !important;
    font-weight: 500 !important;
}

.slider-container input[type=range] {
    background: #334155 !important;
}

.footer {
    text-align: center;
    color: #64748b;
    margin-top: 2rem;
    padding: 1rem;
    border-top: 1px solid #334155;
}
"""

# Image processing functions
def remove_background_simple(image):
    """Simple background removal using color thresholding"""
    if image is None:
        return None
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Convert to RGB if needed
    if len(img_array.shape) == 2:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
    elif img_array.shape[2] == 4:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
    
    # Simple green/white background removal
    # This is a placeholder - real background removal would use ML models
    hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
    
    # Create mask for green backgrounds (common in chroma key)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Invert mask
    mask = cv2.bitwise_not(mask)
    
    # Apply mask
    result = cv2.bitwise_and(img_array, img_array, mask=mask)
    
    # Add alpha channel
    rgba = cv2.cvtColor(result, cv2.COLOR_RGB2RGBA)
    rgba[:, :, 3] = mask
    
    return Image.fromarray(rgba)

def enhance_image(image, brightness=1.0, contrast=1.0, saturation=1.0, sharpness=1.0):
    """Enhance image with various adjustments"""
    if image is None:
        return None
    
    img = image.copy()
    
    # Apply enhancements
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)
    
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast)
    
    if saturation != 1.0:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(saturation)
    
    if sharpness != 1.0:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpness)
    
    return img

def apply_filter(image, filter_type):
    """Apply various filters to image"""
    if image is None:
        return None
    
    img_array = np.array(image)
    
    if filter_type == "Grayscale":
        return Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)).convert('RGB')
    
    elif filter_type == "Sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]])
        sepia = cv2.transform(img_array, kernel)
        sepia = np.clip(sepia, 0, 255).astype(np.uint8)
        return Image.fromarray(sepia)
    
    elif filter_type == "Blur":
        return image.filter(ImageFilter.GaussianBlur(radius=2))
    
    elif filter_type == "Sharpen":
        return image.filter(ImageFilter.SHARPEN)
    
    elif filter_type == "Edge Detection":
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        return Image.fromarray(edges).convert('RGB')
    
    elif filter_type == "Emboss":
        return image.filter(ImageFilter.EMBOSS)
    
    elif filter_type == "Contour":
        return image.filter(ImageFilter.CONTOUR)
    
    elif filter_type == "Detail":
        return image.filter(ImageFilter.DETAIL)
    
    elif filter_type == "Smooth":
        return image.filter(ImageFilter.SMOOTH)
    
    elif filter_type == "Vintage":
        # Apply vintage effect
        img_array = img_array.astype(float)
        img_array[:,:,0] *= 1.1  # Boost red
        img_array[:,:,2] *= 0.9  # Reduce blue
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array)
    
    elif filter_type == "HDR":
        # Simple HDR-like effect
        lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        enhanced = cv2.merge([l, a, b])
        return Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB))
    
    return image

def resize_image(image, width, height, maintain_aspect=True):
    """Resize image with optional aspect ratio preservation"""
    if image is None:
        return None
    
    if maintain_aspect:
        img = image.copy()
        img.thumbnail((width, height), Image.Resampling.LANCZOS)
        return img
    else:
        return image.resize((width, height), Image.Resampling.LANCZOS)

def generate_image_from_text(prompt, width=512, height=512, style="Realistic"):
    """
    Generate image from text prompt
    Note: This is a placeholder. Real implementation would use Stable Diffusion API
    """
    # Create a gradient image as placeholder
    img = Image.new('RGB', (width, height), color='black')
    pixels = img.load()
    
    # Generate gradient based on prompt length (just for visual variety)
    seed = sum(ord(c) for c in prompt)
    np.random.seed(seed)
    
    for i in range(width):
        for j in range(height):
            r = int(128 + 127 * np.sin(i / 50.0 + seed))
            g = int(128 + 127 * np.sin(j / 50.0 + seed))
            b = int(128 + 127 * np.sin((i + j) / 100.0 + seed))
            pixels[i, j] = (r % 256, g % 256, b % 256)
    
    return img

def create_collage(images, layout="Grid"):
    """Create a collage from multiple images"""
    if not images or len(images) == 0:
        return None
    
    # Filter out None values
    images = [img for img in images if img is not None]
    
    if len(images) == 0:
        return None
    
    # Resize all images to same size
    target_size = (300, 300)
    resized = [img.resize(target_size, Image.Resampling.LANCZOS) for img in images]
    
    if layout == "Grid":
        # Calculate grid dimensions
        n = len(resized)
        cols = int(np.ceil(np.sqrt(n)))
        rows = int(np.ceil(n / cols))
        
        # Create collage
        collage_width = cols * 300
        collage_height = rows * 300
        collage = Image.new('RGB', (collage_width, collage_height), color='white')
        
        for idx, img in enumerate(resized):
            row = idx // cols
            col = idx % cols
            collage.paste(img, (col * 300, row * 300))
        
        return collage
    
    elif layout == "Horizontal":
        total_width = len(resized) * 300
        collage = Image.new('RGB', (total_width, 300), color='white')
        for idx, img in enumerate(resized):
            collage.paste(img, (idx * 300, 0))
        return collage
    
    elif layout == "Vertical":
        total_height = len(resized) * 300
        collage = Image.new('RGB', (300, total_height), color='white')
        for idx, img in enumerate(resized):
            collage.paste(img, (0, idx * 300))
        return collage
    
    return resized[0]

def apply_style_transfer(image, style):
    """Apply artistic style to image"""
    if image is None:
        return None
    
    img_array = np.array(image)
    
    if style == "Oil Painting":
        # Oil painting effect
        oil = cv2.xphoto.oilPainting(img_array, size=7, dynRatio=1)
        return Image.fromarray(oil)
    
    elif style == "Pencil Sketch":
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256)
        return Image.fromarray(sketch).convert('RGB')
    
    elif style == "Watercolor":
        # Watercolor-like effect
        res = cv2.stylization(img_array, sigma_s=60, sigma_r=0.6)
        return Image.fromarray(res)
    
    elif style == "Cartoon":
        # Cartoon effect
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        blur = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
        color = cv2.bilateralFilter(img_array, 9, 250, 250)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return Image.fromarray(cartoon)
    
    return image

def add_watermark(image, text, position="Bottom Right", opacity=0.5):
    """Add text watermark to image"""
    if image is None:
        return None
    
    img = image.copy().convert('RGBA')
    watermark = Image.new('RGBA', img.size, (255, 255, 255, 0))
    
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(watermark)
    
    # Try to use a font, fallback to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    # Calculate text size and position
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    if position == "Bottom Right":
        x = img.width - text_width - 20
        y = img.height - text_height - 20
    elif position == "Bottom Left":
        x = 20
        y = img.height - text_height - 20
    elif position == "Top Right":
        x = img.width - text_width - 20
        y = 20
    elif position == "Top Left":
        x = 20
        y = 20
    elif position == "Center":
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
    
    # Draw text with opacity
    alpha = int(255 * opacity)
    draw.text((x, y), text, font=font, fill=(255, 255, 255, alpha))
    
    # Composite images
    result = Image.alpha_composite(img, watermark)
    return result.convert('RGB')

# Build the Gradio interface
with gr.Blocks(css=custom_css, title="AI Image Studio") as demo:
    
    # Header
    gr.HTML("""
    <h1 class="header-text">🎨 AI Image Studio</h1>
    <p class="subheader-text">
        Transform your images with AI-powered editing tools. Upload, edit, enhance, and create stunning visuals!
    </p>
    """)
    
    # Main tabs
    with gr.Tabs():
        
        # Tab 1: Image Generation
        with gr.TabItem("✨ Text to Image"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Generation Settings")
                    prompt_input = gr.Textbox(
                        label="Prompt",
                        placeholder="Describe the image you want to generate...",
                        lines=3
                    )
                    negative_prompt = gr.Textbox(
                        label="Negative Prompt (what to avoid)",
                        placeholder="Things you don't want in the image...",
                        lines=2
                    )
                    
                    with gr.Row():
                        width_slider = gr.Slider(256, 1024, 512, step=64, label="Width")
                        height_slider = gr.Slider(256, 1024, 512, step=64, label="Height")
                    
                    style_dropdown = gr.Dropdown(
                        choices=["Realistic", "Artistic", "Anime", "3D Render", "Sketch"],
                        value="Realistic",
                        label="Style"
                    )
                    
                    generate_btn = gr.Button("🎨 Generate Image", variant="primary")
                    
                    gr.Markdown("""
                    **💡 Tips:**
                    - Be specific in your prompts
                    - Use descriptive adjectives
                    - Mention lighting and mood
                    """)
                
                with gr.Column(scale=1):
                    output_gallery = gr.Gallery(
                        label="Generated Images",
                        show_label=True,
                        elem_classes=["image-preview"],
                        columns=2,
                        rows=2,
                        height=500
                    )
                    
                    # Placeholder generation
                    def generate_placeholder(prompt, width, height, style):
                        img = generate_image_from_text(prompt, width, height, style)
                        return [img]
                    
                    generate_btn.click(
                        fn=generate_placeholder,
                        inputs=[prompt_input, width_slider, height_slider, style_dropdown],
                        outputs=output_gallery
                    )
        
        # Tab 2: Background Removal
        with gr.TabItem("🎯 Background Remover"):
            with gr.Row():
                with gr.Column():
                    bg_input = gr.Image(label="Upload Image", type="pil")
                    remove_btn = gr.Button("🎯 Remove Background", variant="primary")
                
                with gr.Column():
                    bg_output = gr.Image(label="Result", type="pil")
            
            remove_btn.click(
                fn=remove_background_simple,
                inputs=bg_input,
                outputs=bg_output
            )
            
            gr.Markdown("""
            **Note:** This uses a simple color-based removal. For production use, 
            integrate with models like rembg or Stability AI's background removal API.
            """)
        
        # Tab 3: Image Enhancement
        with gr.TabItem("⚡ Image Enhancer"):
            with gr.Row():
                with gr.Column():
                    enhance_input = gr.Image(label="Upload Image", type="pil")
                    
                    gr.Markdown("### Adjustments")
                    brightness = gr.Slider(0.1, 3.0, 1.0, label="Brightness")
                    contrast = gr.Slider(0.1, 3.0, 1.0, label="Contrast")
                    saturation = gr.Slider(0.0, 3.0, 1.0, label="Saturation")
                    sharpness = gr.Slider(0.0, 3.0, 1.0, label="Sharpness")
                    
                    enhance_btn = gr.Button("⚡ Apply Enhancements", variant="primary")
                
                with gr.Column():
                    enhance_output = gr.Image(label="Enhanced Image", type="pil")
            
            enhance_btn.click(
                fn=enhance_image,
                inputs=[enhance_input, brightness, contrast, saturation, sharpness],
                outputs=enhance_output
            )
        
        # Tab 4: Filters
        with gr.TabItem("🎭 Filters & Effects"):
            with gr.Row():
                with gr.Column():
                    filter_input = gr.Image(label="Upload Image", type="pil")
                    
                    filter_type = gr.Dropdown(
                        label="Select Filter",
                        choices=[
                            "Grayscale", "Sepia", "Blur", "Sharpen", 
                            "Edge Detection", "Emboss", "Contour", 
                            "Detail", "Smooth", "Vintage", "HDR"
                        ],
                        value="Grayscale"
                    )
                    
                    apply_filter_btn = gr.Button("🎭 Apply Filter", variant="primary")
                
                with gr.Column():
                    filter_output = gr.Image(label="Filtered Image", type="pil")
            
            apply_filter_btn.click(
                fn=apply_filter,
                inputs=[filter_input, filter_type],
                outputs=filter_output
            )
        
        # Tab 5: Style Transfer
        with gr.TabItem("🖼️ Style Transfer"):
            with gr.Row():
                with gr.Column():
                    style_input = gr.Image(label="Upload Image", type="pil")
                    
                    art_style = gr.Dropdown(
                        label="Artistic Style",
                        choices=["Oil Painting", "Pencil Sketch", "Watercolor", "Cartoon"],
                        value="Oil Painting"
                    )
                    
                    style_btn = gr.Button("🖼️ Apply Style", variant="primary")
                
                with gr.Column():
                    style_output = gr.Image(label="Styled Image", type="pil")
            
            style_btn.click(
                fn=apply_style_transfer,
                inputs=[style_input, art_style],
                outputs=style_output
            )
        
        # Tab 6: Resize & Crop
        with gr.TabItem("📐 Resize & Crop"):
            with gr.Row():
                with gr.Column():
                    resize_input = gr.Image(label="Upload Image", type="pil")
                    
                    with gr.Row():
                        new_width = gr.Number(label="Width (px)", value=512)
                        new_height = gr.Number(label="Height (px)", value=512)
                    
                    maintain_aspect = gr.Checkbox(label="Maintain Aspect Ratio", value=True)
                    resize_btn = gr.Button("📐 Resize Image", variant="primary")
                
                with gr.Column():
                    resize_output = gr.Image(label="Resized Image", type="pil")
            
            resize_btn.click(
                fn=resize_image,
                inputs=[resize_input, new_width, new_height, maintain_aspect],
                outputs=resize_output
            )
        
        # Tab 7: Collage Maker
        with gr.TabItem("🎨 Collage Maker"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("Upload 2-6 images to create a collage")
                    collage_images = gr.Files(label="Upload Images", file_types=["image"])
                    
                    layout_type = gr.Dropdown(
                        label="Layout",
                        choices=["Grid", "Horizontal", "Vertical"],
                        value="Grid"
                    )
                    
                    create_collage_btn = gr.Button("🎨 Create Collage", variant="primary")
                
                with gr.Column():
                    collage_output = gr.Image(label="Collage", type="pil")
            
            def process_collage(files, layout):
                if not files:
                    return None
                images = [Image.open(f.name) for f in files]
                return create_collage(images, layout)
            
            create_collage_btn.click(
                fn=process_collage,
                inputs=[collage_images, layout_type],
                outputs=collage_output
            )
        
        # Tab 8: Watermark
        with gr.TabItem("🔖 Watermark"):
            with gr.Row():
                with gr.Column():
                    wm_input = gr.Image(label="Upload Image", type="pil")
                    wm_text = gr.Textbox(label="Watermark Text", placeholder="Your Name or Brand")
                    
                    wm_position = gr.Dropdown(
                        label="Position",
                        choices=["Bottom Right", "Bottom Left", "Top Right", "Top Left", "Center"],
                        value="Bottom Right"
                    )
                    
                    wm_opacity = gr.Slider(0.1, 1.0, 0.5, label="Opacity")
                    wm_btn = gr.Button("🔖 Add Watermark", variant="primary")
                
                with gr.Column():
                    wm_output = gr.Image(label="Watermarked Image", type="pil")
            
            wm_btn.click(
                fn=add_watermark,
                inputs=[wm_input, wm_text, wm_position, wm_opacity],
                outputs=wm_output
            )
    
    # Footer
    gr.HTML("""
    <div class="footer">
        <p>Built with ❤️ using Gradio | AI Image Studio v1.0</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">
            Note: This demo uses basic image processing. For production AI features, 
            integrate with Stable Diffusion, ControlNet, and other ML models.
        </p>
    </div>
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch(share=True)
