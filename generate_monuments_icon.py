"""
Generate a monuments category icon
"""
import os
from PIL import Image, ImageDraw

icons_dir = 'images/icons'
os.makedirs(icons_dir, exist_ok=True)

def create_monuments_icon(filename):
    """Create an icon representing Indian monuments"""
    img = Image.new('RGB', (200, 200), (240, 245, 250))
    draw = ImageDraw.Draw(img)
    
    # Taj Mahal inspired dome on the left
    draw.ellipse([20, 60, 70, 110], fill=(200, 180, 150), outline=(150, 120, 80), width=2)
    draw.polygon([(45, 50), (55, 60), (35, 60)], fill=(180, 160, 130))
    draw.rectangle([15, 110, 75, 140], fill=(180, 140, 100), outline=(120, 80, 50), width=2)
    
    # Fort/Gate structure in the center-right
    draw.rectangle([85, 80, 155, 140], fill=(180, 100, 50), outline=(100, 50, 20), width=2)
    draw.rectangle([95, 90, 110, 130], fill=(100, 50, 20), outline=(50, 25, 10), width=1)
    draw.rectangle([130, 90, 145, 130], fill=(100, 50, 20), outline=(50, 25, 10), width=1)
    
    # Tower/Minaret on the right
    draw.rectangle([160, 80, 180, 140], fill=(150, 100, 50), outline=(80, 50, 20), width=2)
    draw.polygon([(170, 60), (165, 80), (175, 80)], fill=(130, 80, 40))
    
    # Decorative arch at bottom
    draw.arc([30, 140, 170, 180], 0, 180, fill=(200, 150, 100), width=3)
    
    img.save(filename, 'PNG')
    print(f"✓ Created {filename}")

# Generate the monuments icon
print("Generating monuments category icon...\n")
filepath = os.path.join(icons_dir, 'monuments_icon.png')
create_monuments_icon(filepath)
print("\n✓ Monuments icon created successfully!")
