"""
Generate iconic images for Indian Monuments using PIL
This creates representative icons for each monument
"""
import os
from PIL import Image, ImageDraw
import random

# Create monuments directory if it doesn't exist
monuments_dir = 'images/monuments'
os.makedirs(monuments_dir, exist_ok=True)

def create_image(filename, width=200, height=200, bg_color=(240, 240, 250)):
    """Create a new image with background color"""
    img = Image.new('RGB', (width, height), bg_color)
    return img

def draw_taj_mahal(filename):
    """Draw Taj Mahal - iconic dome with minarets"""
    img = create_image(filename)
    draw = ImageDraw.Draw(img)
    
    # Main dome
    draw.ellipse([70, 60, 130, 120], fill=(220, 220, 220), outline=(100, 100, 100), width=2)
    # Dome top
    draw.polygon([(100, 50), (110, 60), (90, 60)], fill=(200, 180, 150))
    # Base platform
    draw.rectangle([40, 120, 160, 145], fill=(180, 140, 100), outline=(100, 80, 50), width=2)
    # Minarets
    for x in [50, 150]:
        draw.rectangle([x-8, 110, x+8, 145], fill=(150, 150, 150), outline=(80, 80, 80), width=1)
    
    img.save(filename, 'JPEG')
    print(f"✓ Created {filename}")

def draw_india_gate(filename):
    """Draw India Gate - arches and structure"""
    img = create_image(filename)
    draw = ImageDraw.Draw(img)
    
    # Main arch
    draw.arc([60, 50, 140, 130], 0, 180, fill=(139, 69, 19), width=3)
    # Support pillars
    for x in [70, 130]:
        draw.rectangle([x-5, 130, x+5, 160], fill=(139, 69, 19), outline=(80, 40, 10), width=1)
    # Details
    draw.rectangle([80, 60, 120, 100], outline=(200, 150, 100), width=1)
    
    img.save(filename, 'JPEG')
    print(f"✓ Created {filename}")

def draw_hawa_mahal(filename):
    """Draw Hawa Mahal - Pink Palace with windows"""
    img = create_image(filename, bg_color=(255, 240, 245))
    draw = ImageDraw.Draw(img)
    
    # Main structure
    draw.rectangle([50, 80, 150, 160], fill=(255, 182, 193), outline=(200, 100, 120), width=2)
    # Windows
    colors = [(255, 160, 180), (255, 200, 220), (255, 182, 193)]
    for row in range(3):
        for col in range(5):
            x = 60 + col * 16
            y = 90 + row * 18
            draw.rectangle([x, y, x+12, y+12], fill=colors[row % 3], outline=(200, 100, 120), width=1)
    
    img.save(filename, 'JPEG')
    print(f"✓ Created {filename}")

def draw_qutub_minar(filename):
    """Draw Qutub Minar - tall tower"""
    img = create_image(filename)
    draw = ImageDraw.Draw(img)
    
    # Tower base (wider)
    draw.polygon([(80, 120), (120, 120), (110, 80), (90, 80)], fill=(180, 100, 50), outline=(100, 60, 20), width=2)
    # Middle section
    draw.rectangle([85, 60, 115, 85], fill=(160, 80, 40), outline=(80, 40, 10), width=2)
    # Tower top (spire)
    draw.polygon([(100, 30), (95, 60), (105, 60)], fill=(140, 60, 20), outline=(80, 40, 10), width=2)
    # Decorative rings
    for y in [75, 95]:
        draw.ellipse([85, y-2, 115, y+2], fill=(120, 60, 30))
    
    img.save(filename, 'JPEG')
    print(f"✓ Created {filename}")

def draw_gateway_of_india(filename):
    """Draw Gateway of India - grand arch"""
    img = create_image(filename)
    draw = ImageDraw.Draw(img)
    
    # Main arch
    draw.arc([50, 40, 150, 140], 0, 180, fill=(139, 69, 19), width=4)
    # Supports
    draw.rectangle([60, 135, 75, 160], fill=(180, 100, 50), outline=(100, 60, 20), width=2)
    draw.rectangle([125, 135, 140, 160], fill=(180, 100, 50), outline=(100, 60, 20), width=2)
    # Decorative elements
    draw.circle((100, 70), 8, fill=(200, 150, 100))
    
    img.save(filename, 'JPEG')
    print(f"✓ Created {filename}")

def draw_red_fort(filename):
    """Draw Red Fort - fortress with walls"""
    img = create_image(filename, bg_color=(240, 240, 250))
    draw = ImageDraw.Draw(img)
    
    # Outer wall
    draw.rectangle([40, 50, 160, 150], fill=(200, 80, 50), outline=(100, 40, 20), width=3)
    # Inner structure
    draw.rectangle([60, 70, 140, 130], fill=(240, 150, 100), outline=(100, 50, 30), width=2)
    # Towers
    for x in [45, 155]:
        draw.rectangle([x-8, 45, x+8, 60], fill=(150, 60, 30), outline=(80, 30, 10), width=1)
    # Gate
    draw.rectangle([95, 150, 105, 170], fill=(100, 40, 20), outline=(50, 20, 10), width=1)
    
    img.save(filename, 'JPEG')
    print(f"✓ Created {filename}")

def draw_statue_of_unity(filename):
    """Draw Statue of Unity - tall figure"""
    img = create_image(filename)
    draw = ImageDraw.Draw(img)
    
    # Head
    draw.ellipse([85, 30, 115, 60], fill=(210, 170, 120), outline=(150, 120, 80), width=2)
    # Body
    draw.rectangle([80, 60, 120, 120], fill=(200, 150, 100), outline=(150, 100, 60), width=2)
    # Arms
    draw.line([(80, 80), (50, 90)], fill=(200, 150, 100), width=8)
    draw.line([(120, 80), (150, 90)], fill=(200, 150, 100), width=8)
    # Legs
    draw.rectangle([85, 120, 95, 160], fill=(150, 100, 60), outline=(100, 60, 30), width=1)
    draw.rectangle([105, 120, 115, 160], fill=(150, 100, 60), outline=(100, 60, 30), width=1)
    
    img.save(filename, 'JPEG')
    print(f"✓ Created {filename}")

def draw_temple(filename, title="Temple"):
    """Generic temple drawing"""
    img = create_image(filename)
    draw = ImageDraw.Draw(img)
    
    # Main temple structure
    draw.polygon([(100, 30), (80, 80), (120, 80)], fill=(200, 100, 50), outline=(100, 50, 20), width=2)
    # Base
    draw.rectangle([60, 80, 140, 160], fill=(150, 80, 40), outline=(80, 40, 20), width=2)
    # Entrance
    draw.rectangle([90, 100, 110, 130], fill=(100, 50, 20), outline=(50, 25, 10), width=1)
    # Pillars
    draw.rectangle([70, 130, 80, 160], fill=(120, 60, 30))
    draw.rectangle([120, 130, 130, 160], fill=(120, 60, 30))
    
    img.save(filename, 'JPEG')
    print(f"✓ Created {filename}")

def draw_mosque(filename):
    """Draw mosque - dome and minarets"""
    img = create_image(filename)
    draw = ImageDraw.Draw(img)
    
    # Main dome
    draw.ellipse([75, 60, 125, 110], fill=(100, 150, 200), outline=(50, 100, 150), width=2)
    # Base
    draw.rectangle([50, 110, 150, 160], fill=(200, 150, 100), outline=(100, 80, 50), width=2)
    # Minarets
    for x in [55, 145]:
        draw.rectangle([x-6, 95, x+6, 155], fill=(100, 150, 200), outline=(50, 100, 150), width=1)
        draw.circle((x, 90), 5, fill=(150, 200, 255))
    
    img.save(filename, 'JPEG')
    print(f"✓ Created {filename}")

def draw_palace(filename):
    """Draw palace - grand structure"""
    img = create_image(filename, bg_color=(255, 250, 240))
    draw = ImageDraw.Draw(img)
    
    # Main palace
    draw.rectangle([40, 70, 160, 150], fill=(210, 180, 140), outline=(150, 120, 80), width=2)
    # Central tower
    draw.rectangle([85, 40, 115, 70], fill=(180, 150, 110), outline=(130, 100, 60), width=2)
    # Windows
    for row in range(2):
        for col in range(4):
            x = 55 + col * 26
            y = 85 + row * 30
            draw.rectangle([x, y, x+16, y+16], fill=(220, 200, 150), outline=(100, 80, 50), width=1)
    
    img.save(filename, 'JPEG')
    print(f"✓ Created {filename}")

def draw_fort(filename):
    """Draw generic fort"""
    img = create_image(filename)
    draw = ImageDraw.Draw(img)
    
    # Walls
    draw.rectangle([40, 60, 160, 140], fill=(170, 100, 50), outline=(80, 40, 20), width=3)
    # Towers at corners
    for pos in [(40, 60), (160, 60), (40, 140), (160, 140)]:
        draw.rectangle([pos[0]-12, pos[1]-12, pos[0]+12, pos[1]+12], fill=(150, 80, 40), outline=(80, 40, 20), width=2)
    # Gate
    draw.rectangle([95, 140, 105, 170], fill=(80, 40, 20))
    
    img.save(filename, 'JPEG')
    print(f"✓ Created {filename}")

# Generate all monument icons
print("Generating Indian Monument icons...\n")

monuments = {
    'taj_mahal.jpg': draw_taj_mahal,
    'india_gate.jpg': draw_india_gate,
    'hawa_mahal.jpg': draw_hawa_mahal,
    'qutub_minar.jpg': draw_qutub_minar,
    'gateway_of_india.jpg': draw_gateway_of_india,
    'red_fort.jpg': draw_red_fort,
    'statue_of_unity.jpg': draw_statue_of_unity,
}

# Generate specific monuments
for filename, draw_func in monuments.items():
    filepath = os.path.join(monuments_dir, filename)
    draw_func(filepath)

# Generate remaining monuments with generic templates
remaining_monuments = [
    'ramakrishna_mission.jpg', 'victoria_memorial.jpg', 'mysore_palace.jpg',
    'charminar.jpg', 'buland_darwaza.jpg', 'amber_fort.jpg', 'meenakshi_temple.jpg',
    'varanasi_ghats.jpg', 'khajuraho_temples.jpg', 'konark_sun_temple.jpg',
    'sanchi_stupa.jpg', 'ajanta_caves.jpg', 'ellora_caves.jpg', 'badami_caves.jpg',
    'mahabalipuram.jpg', 'hampi.jpg', 'raigad_fort.jpg', 'jaisalmer_fort.jpg',
    'jodhpur_fort.jpg', 'udaipur_palace.jpg', 'amer_palace.jpg', 'humayun_tomb.jpg',
    'akbar_tomb.jpg', 'fatehpur_sikri.jpg', 'bijapur_gol_gumbaz.jpg',
    'minar_e_pakistan.jpg', 'darjeeling_himalayan_railway.jpg', 'nalanda_university.jpg',
    'sarnath_stupa.jpg', 'bodhgaya_temple.jpg', 'ranthambore_fort.jpg',
    'chittor_fort.jpg', 'goa_basilica.jpg'
]

# Generate remaining with templates
for filename in remaining_monuments:
    filepath = os.path.join(monuments_dir, filename)
    if 'palace' in filename:
        draw_palace(filepath)
    elif 'temple' in filename or 'gumbaz' in filename or 'stupa' in filename or 'basilica' in filename:
        draw_temple(filepath)
    elif 'mosque' in filename:
        draw_mosque(filepath)
    elif 'fort' in filename or 'raigad' in filename or 'jaisalmer' in filename or 'jodhpur' in filename or 'chittor' in filename or 'ranthambore' in filename:
        draw_fort(filepath)
    elif 'caves' in filename or 'mahabalipuram' in filename or 'hampi' in filename:
        # Draw cave-like structure
        img = create_image(filepath)
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 80, 150, 150], fill=(120, 100, 80), outline=(70, 50, 30), width=3)
        draw.ellipse([60, 90, 140, 130], fill=(100, 80, 60), outline=(60, 40, 20), width=2)
        img.save(filepath, 'JPEG')
        print(f"✓ Created {filepath}")
    elif 'railway' in filename:
        # Draw railway/train
        img = create_image(filepath)
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 100, 150, 140], fill=(200, 100, 50), outline=(100, 50, 20), width=2)
        draw.circle((60, 140), 15, fill=(80, 80, 80))
        draw.circle((110, 140), 15, fill=(80, 80, 80))
        img.save(filepath, 'JPEG')
        print(f"✓ Created {filepath}")
    elif 'university' in filename:
        # Draw university building
        img = create_image(filepath)
        draw = ImageDraw.Draw(img)
        draw.rectangle([40, 70, 160, 150], fill=(180, 120, 80), outline=(100, 60, 30), width=2)
        for row in range(3):
            for col in range(4):
                x = 55 + col * 26
                y = 85 + row * 20
                draw.rectangle([x, y, x+16, y+16], fill=(255, 255, 200), outline=(150, 120, 80), width=1)
        img.save(filepath, 'JPEG')
        print(f"✓ Created {filepath}")
    else:
        draw_fort(filepath)

print("\n✓ All 40 monument icons generated successfully!")
print(f"Icons are saved in the '{monuments_dir}' folder\n")

# Count generated files
generated_files = [f for f in os.listdir(monuments_dir) if f.endswith('.jpg')]
print(f"Total monuments created: {len(generated_files)}")
