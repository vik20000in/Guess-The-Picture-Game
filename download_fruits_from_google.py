import requests
from bs4 import BeautifulSoup
import re
import os
import time
from PIL import Image
from io import BytesIO

# Create fruits directory if it doesn't exist
base_path = os.path.dirname(os.path.abspath(__file__))
fruits_dir = os.path.join(base_path, 'images', 'fruits')
os.makedirs(fruits_dir, exist_ok=True)

# List of fruits to download
fruits = [
    'mango',
    'banana',
    'apple',
    'papaya',
    'coconut',
    'guava',
    'pomegranate',
    'watermelon',
    'pineapple',
    'orange',
    'lemon',
    'lime',
    'grapes',
    'strawberry',
    'blueberry',
    'raspberry',
    'blackberry',
    'kiwi',
    'peach',
    'pear',
    'plum',
    'apricot',
    'cherry',
    'dragon fruit',
    'avocado',
    'passion fruit',
    'fig',
    'date',
    'litchi',
    'longan',
    'jackfruit',
    'custard apple',
    'sugar cane',
    'carambola',
    'mulberry',
    'tamarind',
    'grapefruit',
    'tangerine',
    'melon',
    'honeydew'
]

def download_image_from_google(query, save_path, max_retries=3):
    """
    Download first image from Google Images for given query
    """
    for attempt in range(max_retries):
        try:
            url = "https://www.google.com/search?q=" + query.replace(" ", "+") + "&tbm=isch"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

            response = requests.get(url, headers=headers, timeout=15)
            html = response.text

            # Find the first image source from the script tag
            match = re.search(r'"ou":"(.*?)"', html)
            if not match:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return False

            img_url = match.group(1)
            
            # Download the image
            img_response = requests.get(img_url, headers=headers, timeout=15)
            
            if img_response.status_code == 200:
                # Try to open and verify it's a valid image
                img = Image.open(BytesIO(img_response.content))
                
                # Convert to RGB if needed
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                img.save(save_path, 'JPEG')
                return True
            
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
            continue
    
    return False

# Download images for each fruit
print("=" * 60)
print("Downloading FRUIT images from Google...")
print("=" * 60)

successful = 0
failed = 0
failed_fruits = []

for idx, fruit in enumerate(fruits, 1):
    # Convert fruit name to valid filename (replace spaces with underscores)
    filename = fruit.replace(" ", "_")
    save_path = os.path.join(fruits_dir, f"{filename}.jpg")
    
    print(f"\n[{idx}/40] [{fruit.upper()}]", end=" ")
    
    # Check if image already exists
    if os.path.exists(save_path):
        try:
            file_size = os.path.getsize(save_path) / 1024
            print(f"✓ Already exists ({file_size:.1f} KB)")
            successful += 1
        except:
            print(f"✓ Already exists")
            successful += 1
    else:
        print(f"Downloading...", end="", flush=True)
        if download_image_from_google(fruit, save_path):
            try:
                file_size = os.path.getsize(save_path) / 1024
                print(f" ✓ ({file_size:.1f} KB)")
                successful += 1
            except:
                print(f" ✓ Downloaded")
                successful += 1
        else:
            print(f" ✗ Failed")
            failed += 1
            failed_fruits.append(fruit)
    
    time.sleep(1)  # Rate limiting

print("\n" + "=" * 60)
print("Download complete!")
print("=" * 60)
total = len(fruits)
print(f"\n✓ Successfully downloaded: {successful}/{total}")
if failed > 0:
    print(f"✗ Failed: {failed}/{total}")
    print(f"\nFailed fruits: {', '.join(failed_fruits)}")

# Verify downloaded files
print("\n" + "=" * 60)
print("Verifying downloaded files...")
print("=" * 60)
downloaded_files = os.listdir(fruits_dir)
print(f"Total files in fruits folder: {len(downloaded_files)}")
for file in sorted(downloaded_files):
    file_size = os.path.getsize(os.path.join(fruits_dir, file)) / 1024
    print(f"  ✓ {file} ({file_size:.1f} KB)")
