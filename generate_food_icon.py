from PIL import Image, ImageDraw

# Create food icon
size = (100, 100)
background_color = (255, 255, 255)
line_color = (0, 0, 0)
food_color = (255, 165, 0)  # Orange for food

food_icon = Image.new('RGB', size, background_color)
draw = ImageDraw.Draw(food_icon)

# Draw plate (circle)
draw.ellipse([15, 30, 85, 80], fill=background_color, outline=line_color, width=2)

# Draw some food items on the plate
# Rice/food mound
draw.polygon([(50, 40), (35, 60), (65, 60)], fill=food_color, outline=line_color)

# Spoon
draw.ellipse([20, 50, 30, 65], fill=(200, 150, 100), outline=line_color, width=2)
draw.rectangle([22, 65, 28, 75], fill=(200, 150, 100), outline=line_color, width=2)

# Fork
fork_color = (200, 200, 200)
draw.rectangle([70, 40, 75, 75], fill=fork_color, outline=line_color, width=1)
draw.rectangle([70, 75, 75, 80], fill=fork_color, outline=line_color, width=1)
# Fork prongs
draw.rectangle([68, 75, 72, 85], fill=fork_color, outline=line_color, width=1)
draw.rectangle([76, 75, 80, 85], fill=fork_color, outline=line_color, width=1)

food_icon.save('images/icons/food_icon.png')
print("Created food_icon.png")
