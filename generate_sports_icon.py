from PIL import Image, ImageDraw

# Create sports icon
size = (100, 100)
background_color = (255, 255, 255)
line_color = (0, 0, 0)
sports_color = (220, 20, 60)  # Crimson red for sports

sports_icon = Image.new('RGB', size, background_color)
draw = ImageDraw.Draw(sports_icon)

# Draw a soccer ball (football)
# Circle outline
draw.ellipse([20, 20, 80, 80], outline=line_color, width=2)

# Pentagon pattern on soccer ball
# Draw some pentagons and hexagons for soccer ball pattern
draw.polygon([(50, 25), (60, 35), (55, 45), (45, 45), (40, 35)], outline=line_color, width=1)
draw.polygon([(50, 55), (60, 65), (55, 75), (45, 75), (40, 65)], outline=line_color, width=1)
draw.polygon([(25, 50), (35, 45), (45, 50), (40, 60), (30, 60)], outline=line_color, width=1)
draw.polygon([(55, 50), (65, 45), (75, 50), (70, 60), (60, 60)], outline=line_color, width=1)

# Draw a bat/racket on the side
# Tennis racket
draw.ellipse([8, 25, 18, 35], outline=sports_color, width=2, fill=sports_color)
draw.rectangle([10, 35, 16, 70], fill=sports_color, outline=line_color, width=1)

# Draw a small ball
draw.ellipse([82, 82, 90, 90], fill=sports_color, outline=line_color, width=1)

sports_icon.save('images/icons/sports_icon.png')
print("Created sports_icon.png")
