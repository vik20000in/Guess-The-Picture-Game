from PIL import Image, ImageDraw
import os

# Create icons directory if it doesn't exist
icons_dir = 'images/icons'
os.makedirs(icons_dir, exist_ok=True)

# Icon size
size = (100, 100)
background_color = (255, 255, 255)
line_color = (0, 0, 0)
fill_color = (100, 150, 255)

# 1. Animal Icon - Simple lion/animal face
animal_icon = Image.new('RGB', size, background_color)
draw = ImageDraw.Draw(animal_icon)

# Draw circle for head
draw.ellipse([20, 20, 80, 80], fill=fill_color, outline=line_color, width=2)
# Draw ears
draw.ellipse([25, 15, 35, 30], fill=fill_color, outline=line_color, width=2)
draw.ellipse([65, 15, 75, 30], fill=fill_color, outline=line_color, width=2)
# Draw eyes
draw.ellipse([35, 40, 40, 45], fill=line_color)
draw.ellipse([60, 40, 65, 45], fill=line_color)
# Draw nose
draw.ellipse([48, 55, 52, 59], fill=line_color)
# Draw mouth
draw.arc([35, 55, 65, 70], 0, 180, fill=line_color, width=2)

animal_icon.save(os.path.join(icons_dir, 'animal_icon.png'))
print("Created animal_icon.png")

# 2. Things Icon - Simple house
things_icon = Image.new('RGB', size, background_color)
draw = ImageDraw.Draw(things_icon)

# Draw house base (rectangle)
draw.rectangle([25, 40, 75, 75], fill=fill_color, outline=line_color, width=2)
# Draw roof (triangle)
draw.polygon([(25, 40), (50, 15), (75, 40)], fill=fill_color, outline=line_color)
# Draw door
draw.rectangle([43, 55, 57, 75], fill=(180, 100, 50), outline=line_color, width=2)
# Draw door knob
draw.ellipse([54, 63, 57, 66], fill=line_color)
# Draw window
draw.rectangle([30, 45, 40, 55], fill=(100, 200, 255), outline=line_color, width=2)

things_icon.save(os.path.join(icons_dir, 'thing_icon.png'))
print("Created thing_icon.png")

# 3. Bollywood Icon - Simple film reel/star
bollywood_icon = Image.new('RGB', size, background_color)
draw = ImageDraw.Draw(bollywood_icon)

# Draw star
star_color = (255, 215, 0)  # Gold color
star_points = [
    (50, 15),   # top
    (61, 40),   # top right
    (85, 40),   # right
    (68, 57),   # bottom right
    (75, 80),   # bottom
    (50, 63),   # center
    (25, 80),   # bottom left
    (32, 57),   # top left
    (15, 40),   # left
    (39, 40),   # top left
]
draw.polygon(star_points, fill=star_color, outline=line_color, width=2)

bollywood_icon.save(os.path.join(icons_dir, 'bollywood_icon.png'))
print("Created bollywood_icon.png")

print("All icons generated successfully!")
