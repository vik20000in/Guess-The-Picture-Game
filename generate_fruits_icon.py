"""
Generate Fruits category icon
"""
import os
from PIL import Image, ImageDraw

icons_dir = 'images/icons'
os.makedirs(icons_dir, exist_ok=True)

def create_fruits_icon(filename):
    """Create an icon representing fruits"""
    img = Image.new('RGB', (200, 200), (240, 250, 240))
    draw = ImageDraw.Draw(img)
    
    # Mango (left side, orange-yellow)
    draw.ellipse([20, 60, 80, 120], fill=(255, 200, 0), outline=(200, 150, 0), width=2)
    draw.polygon([(50, 50), (60, 60), (40, 60)], fill=(200, 150, 0))
    
    # Apple (top middle, red)
    draw.ellipse([90, 40, 140, 90], fill=(255, 100, 100), outline=(200, 50, 50), width=2)
    draw.circle((115, 35), 8, fill=(100, 200, 100))
    
    # Banana (right side, yellow)
    draw.arc([140, 70, 180, 130], 0, 180, fill=(255, 255, 0), width=3)
    
    # Grapes (bottom left, purple)
    for i in range(3):
        for j in range(3):
            draw.circle((35 + i*15, 140 + j*15), 8, fill=(150, 100, 200), outline=(100, 50, 150), width=1)
    
    # Watermelon (bottom right, red/green)
    draw.ellipse([140, 130, 190, 180], fill=(200, 50, 50), outline=(100, 25, 25), width=2)
    draw.arc([150, 140, 180, 170], 0, 360, fill=(100, 200, 100), width=2)
    
    img.save(filename, 'PNG')
    print(f"✓ Created {filename}")

# Generate the fruits icon
print("Generating fruits category icon...\n")
filepath = os.path.join(icons_dir, 'fruits_icon.png')
create_fruits_icon(filepath)
print("\n✓ Fruits icon created successfully!")
