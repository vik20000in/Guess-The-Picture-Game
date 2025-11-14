import os
from PIL import Image, ImageDraw, ImageFont

# Paths
base_path = os.path.dirname(os.path.abspath(__file__))
animals_dir = os.path.join(base_path, 'images', 'animals')
things_dir = os.path.join(base_path, 'images', 'things')
bollywood_dir = os.path.join(base_path, 'images', 'bollywood')

# Expected items from script.js
expected = {
    'animals': ['Lion', 'Elephant', 'Giraffe', 'Zebra', 'Monkey', 'Tiger', 'Bear', 'Dog', 'Cat', 'Penguin'],
    'things': ['Car', 'Ball', 'House', 'Tree', 'Book', 'Chair', 'Table', 'Phone', 'Umbrella', 'Bicycle'],
    'bollywood': ['Shah Rukh Khan', 'Amitabh Bachchan', 'Salman Khan', 'Deepika Padukone', 'Hrithik Roshan', 
                  'Priyanka Chopra', 'Aamir Khan', 'Alia Bhatt', 'Ranbir Kapoor', 'Katrina Kaif']
}

expected_filenames = {
    'animals': {
        'Lion': 'lion.png',
        'Elephant': 'elephant.png',
        'Giraffe': 'giraffe.png',
        'Zebra': 'zebra.png',
        'Monkey': 'monkey.png',
        'Tiger': 'tiger.png',
        'Bear': 'bear.png',
        'Dog': 'dog.png',
        'Cat': 'cat.png',
        'Penguin': 'penguin.png',
    },
    'things': {
        'Car': 'car.png',
        'Ball': 'ball.png',
        'House': 'house.png',
        'Tree': 'tree.png',
        'Book': 'book.png',
        'Chair': 'chair.png',
        'Table': 'table.png',
        'Phone': 'phone.png',
        'Umbrella': 'umbrella.png',
        'Bicycle': 'bicycle.png',
    },
    'bollywood': {
        'Shah Rukh Khan': 'srk.png',
        'Amitabh Bachchan': 'amitabh.png',
        'Salman Khan': 'salman.png',
        'Deepika Padukone': 'deepika.png',
        'Hrithik Roshan': 'hrithik.png',
        'Priyanka Chopra': 'priyanka.png',
        'Aamir Khan': 'aamir.png',
        'Alia Bhatt': 'alia.png',
        'Ranbir Kapoor': 'ranbir.png',
        'Katrina Kaif': 'katrina.png',
    }
}

def create_placeholder_image(save_path, text):
    """Create a placeholder image for missing items"""
    try:
        img = Image.new('RGB', (400, 300), color=(100, 150, 200))
        draw = ImageDraw.Draw(img)
        
        # Split text into multiple lines if it's too long
        lines = text.split()
        if len(lines) > 2:
            lines = [' '.join(lines[:len(lines)//2]), ' '.join(lines[len(lines)//2:])]
        
        # Calculate text position
        y_offset = 0
        for line in lines:
            try:
                bbox = draw.textbbox((0, 0), line)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except:
                text_width = len(line) * 8
                text_height = 15
            
            x = (400 - text_width) // 2
            y = (300 - text_height * len(lines)) // 2 + y_offset
            
            draw.text((x, y), line, fill='white')
            y_offset += text_height + 10
        
        img.save(save_path, 'PNG')
        return True
    except Exception as e:
        print(f"Error creating placeholder for {text}: {e}")
        return False

# Check and create missing images
print("=" * 60)
print("Image Status Report")
print("=" * 60)

for category, items in expected.items():
    if category == 'animals':
        dir_path = animals_dir
    elif category == 'things':
        dir_path = things_dir
    else:
        dir_path = bollywood_dir
    
    print(f"\n{category.upper()}:")
    print("-" * 60)
    
    missing_count = 0
    existing_count = 0
    
    for item in items:
        filename = expected_filenames[category][item]
        file_path = os.path.join(dir_path, filename)
        
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path) / 1024  # KB
            print(f"  ✓ {item:<25} ({file_size:.1f} KB)")
            existing_count += 1
        else:
            print(f"  ✗ {item:<25} [CREATING PLACEHOLDER]")
            create_placeholder_image(file_path, item)
            missing_count += 1
    
    print(f"\n  Summary: {existing_count} downloaded, {missing_count} placeholder")

print("\n" + "=" * 60)
print("✓ All required images are now available!")
print("=" * 60)
