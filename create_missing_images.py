import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Create directories if they don't exist
base_path = os.path.dirname(os.path.abspath(__file__))
animals_dir = os.path.join(base_path, 'images', 'animals')
things_dir = os.path.join(base_path, 'images', 'things')

def create_high_quality_placeholder(save_path, text, bg_color=(100, 150, 200)):
    """Create a high-quality placeholder image"""
    try:
        # Create a larger canvas for better quality
        width, height = 800, 600
        img = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Add gradient effect by drawing semi-transparent rectangles
        for i in range(height):
            color_value = int(bg_color[0] + (255 - bg_color[0]) * (i / height))
            draw.rectangle([(0, i), (width, i+1)], fill=(color_value, color_value + 30, color_value + 60))
        
        # Draw text with shadow
        text_lines = text.split()
        if len(text_lines) > 2:
            text_lines = [' '.join(text_lines[:len(text_lines)//2]), ' '.join(text_lines[len(text_lines)//2:])]
        
        font_size = int(height * 0.15)
        
        # Draw shadow
        for line_idx, line in enumerate(text_lines):
            y_offset = (height - font_size * len(text_lines)) // 2 + line_idx * (font_size + 20)
            
            # Rough text estimation for positioning
            text_width_estimate = len(line) * (font_size * 0.6)
            x = (width - text_width_estimate) // 2
            
            # Draw shadow (black text offset)
            draw.text((x+3, y_offset+3), line, fill=(0, 0, 0), font=None)
            # Draw main text (white)
            draw.text((x, y_offset), line, fill=(255, 255, 255), font=None)
        
        # Resize down to target size
        img = img.resize((400, 300), Image.Resampling.LANCZOS)
        img.save(save_path, 'PNG')
        return True
    except Exception as e:
        print(f"Error creating placeholder for {text}: {e}")
        return False

# Create missing animal images
print("Creating missing animal images...")
if not os.path.exists(os.path.join(animals_dir, 'elephant.png')):
    print("  Creating ELEPHANT placeholder...")
    create_high_quality_placeholder(os.path.join(animals_dir, 'elephant.png'), 'ELEPHANT', (150, 100, 80))

if not os.path.exists(os.path.join(animals_dir, 'bear.png')):
    print("  Creating BEAR placeholder...")
    create_high_quality_placeholder(os.path.join(animals_dir, 'bear.png'), 'BEAR', (120, 80, 60))

# Create missing thing images
print("Creating missing thing images...")
if not os.path.exists(os.path.join(things_dir, 'ball.png')):
    print("  Creating BALL placeholder...")
    create_high_quality_placeholder(os.path.join(things_dir, 'ball.png'), 'BALL', (200, 50, 50))

print("✓ All missing images created!")
