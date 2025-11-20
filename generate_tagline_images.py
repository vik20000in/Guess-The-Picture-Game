import json
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Load taglines data
with open('data/taglines.json', 'r', encoding='utf-8') as f:
    taglines = json.load(f)

# Create output directory if it doesn't exist
os.makedirs('images/taglines', exist_ok=True)

# Image settings
IMG_WIDTH = 800
IMG_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (0, 0, 0)  # Black
PADDING = 60

def create_tagline_image(tagline_text, company_name, output_path):
    """Create an image with the tagline text centered"""
    # Create image
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Try to load a nice font, fallback to default if not available
    try:
        # Try different font sizes for best fit
        font_size = 80
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Wrap text if it's too long
    max_chars_per_line = 25
    wrapped_lines = textwrap.wrap(tagline_text, width=max_chars_per_line)
    
    # Calculate total text height
    line_height = font_size + 20
    total_text_height = len(wrapped_lines) * line_height
    
    # Start y position to center the text vertically
    y_position = (IMG_HEIGHT - total_text_height) // 2
    
    # Draw each line centered
    for line in wrapped_lines:
        # Get text bounding box to center it
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_position = (IMG_WIDTH - text_width) // 2
        
        # Draw the text
        draw.text((x_position, y_position), line, fill=TEXT_COLOR, font=font)
        y_position += line_height
    
    # Add quotation marks decoratively
    try:
        quote_font = ImageFont.truetype("arial.ttf", 120)
    except:
        quote_font = font
    
    # Left quote
    draw.text((PADDING, PADDING), '"', fill=(200, 200, 200), font=quote_font)
    # Right quote
    draw.text((IMG_WIDTH - PADDING - 60, IMG_HEIGHT - PADDING - 100), '"', fill=(200, 200, 200), font=quote_font)
    
    # Save the image
    img.save(output_path, 'JPEG', quality=95)
    print(f"Created: {output_path}")

# Generate images for all taglines
for item in taglines:
    tagline_text = item['tagline']
    company_name = item['name']
    filename = item['image'].split('/')[-1]
    output_path = f"images/taglines/{filename}"
    
    create_tagline_image(tagline_text, company_name, output_path)

print(f"\nSuccessfully created {len(taglines)} tagline images!")
