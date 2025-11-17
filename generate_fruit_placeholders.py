"""
Generate placeholder fruit images for quick testing
Creates simple colored images representing each fruit
"""
import os
from PIL import Image, ImageDraw

fruits_dir = 'images/fruits'
os.makedirs(fruits_dir, exist_ok=True)

fruits_config = [
    ('mango.jpg', 'Mango', (255, 200, 0), '#FFD700'),
    ('banana.jpg', 'Banana', (255, 255, 0), '#FFFF00'),
    ('apple.jpg', 'Apple', (255, 100, 100), '#FF6464'),
    ('papaya.jpg', 'Papaya', (255, 165, 100), '#FFA564'),
    ('coconut.jpg', 'Coconut', (200, 200, 200), '#C8C8C8'),
    ('guava.jpg', 'Guava', (150, 200, 100), '#96C864'),
    ('pomegranate.jpg', 'Pomegranate', (200, 100, 100), '#C86464'),
    ('watermelon.jpg', 'Watermelon', (200, 50, 50), '#C83232'),
    ('pineapple.jpg', 'Pineapple', (255, 215, 0), '#FFD700'),
    ('orange.jpg', 'Orange', (255, 165, 0), '#FFA500'),
    ('lemon.jpg', 'Lemon', (255, 255, 100), '#FFFF64'),
    ('lime.jpg', 'Lime', (150, 255, 100), '#96FF64'),
    ('grapes.jpg', 'Grapes', (150, 100, 200), '#9664C8'),
    ('strawberry.jpg', 'Strawberry', (255, 100, 100), '#FF6464'),
    ('blueberry.jpg', 'Blueberry', (100, 100, 200), '#6464C8'),
    ('raspberry.jpg', 'Raspberry', (180, 100, 150), '#B46496'),
    ('blackberry.jpg', 'Blackberry', (100, 50, 100), '#643264'),
    ('kiwi.jpg', 'Kiwi', (150, 200, 100), '#96C864'),
    ('peach.jpg', 'Peach', (255, 200, 150), '#FFC896'),
    ('pear.jpg', 'Pear', (200, 200, 100), '#C8C864'),
    ('plum.jpg', 'Plum', (180, 100, 180), '#B464B4'),
    ('apricot.jpg', 'Apricot', (255, 180, 100), '#FFB464'),
    ('cherry.jpg', 'Cherry', (200, 50, 50), '#C83232'),
    ('dragon_fruit.jpg', 'Dragon Fruit', (255, 100, 150), '#FF6496'),
    ('avocado.jpg', 'Avocado', (100, 150, 100), '#649664'),
    ('passion_fruit.jpg', 'Passion Fruit', (200, 100, 50), '#C86432'),
    ('fig.jpg', 'Fig', (150, 100, 150), '#9664966'),
    ('date.jpg', 'Date', (139, 90, 50), '#8B5A32'),
    ('litchi.jpg', 'Litchi', (255, 100, 150), '#FF6496'),
    ('longan.jpg', 'Longan', (200, 150, 100), '#C89664'),
    ('jackfruit.jpg', 'Jackfruit', (255, 215, 0), '#FFD700'),
    ('custard_apple.jpg', 'Custard Apple', (200, 200, 150), '#C8C896'),
    ('sugar_cane.jpg', 'Sugar Cane', (200, 200, 100), '#C8C864'),
    ('carambola.jpg', 'Carambola', (255, 255, 100), '#FFFF64'),
    ('mulberry.jpg', 'Mulberry', (150, 50, 150), '#963296'),
    ('tamarind.jpg', 'Tamarind', (150, 100, 50), '#966432'),
    ('grapefruit.jpg', 'Grapefruit', (255, 180, 150), '#FFB496'),
    ('tangerine.jpg', 'Tangerine', (255, 150, 0), '#FF9600'),
    ('melon.jpg', 'Melon', (200, 200, 100), '#C8C864'),
    ('honeydew.jpg', 'Honeydew', (200, 255, 100), '#C8FF64'),
]

print("\n🍎 Generating placeholder fruit images...\n")

for filename, name, color, hex_color in fruits_config:
    filepath = os.path.join(fruits_dir, filename)
    
    # Create a simple colored image
    img = Image.new('RGB', (400, 400), color)
    draw = ImageDraw.Draw(img)
    
    # Draw a simple fruit shape (circle/ellipse)
    margin = 50
    draw.ellipse([margin, margin, 400-margin, 400-margin], 
                 fill=color, outline=(0, 0, 0), width=3)
    
    # Add text label
    draw.text((200, 180), name, fill=(0, 0, 0), anchor="mm",
              font=None)
    
    # Save the image
    img.save(filepath, 'JPEG', quality=85)
    print(f"✅ Created: {filename}")

print(f"\n✅ All 40 placeholder fruit images created!\n")
