import os
import requests
from PIL import Image
from io import BytesIO
import time
from urllib.parse import quote
import re

# Create directories if they don't exist
base_path = os.path.dirname(os.path.abspath(__file__))
animals_dir = os.path.join(base_path, 'images', 'animals')
things_dir = os.path.join(base_path, 'images', 'things')
bollywood_dir = os.path.join(base_path, 'images', 'bollywood')

os.makedirs(animals_dir, exist_ok=True)
os.makedirs(things_dir, exist_ok=True)
os.makedirs(bollywood_dir, exist_ok=True)

# Define search queries with better keywords
animals = {
    'lion': 'Lion animal wildlife',
    'elephant': 'Elephant animal wildlife',
    'giraffe': 'Giraffe animal wildlife',
    'zebra': 'Zebra animal wildlife',
    'monkey': 'Monkey primate animal',
    'tiger': 'Tiger animal wildlife',
    'bear': 'Bear animal wildlife',
    'dog': 'Dog puppy pet',
    'cat': 'Cat kitten pet',
    'penguin': 'Penguin bird animal',
}

# Things to download
things = {
    'car': 'Car automobile vehicle',
    'ball': 'Ball sports round',
    'house': 'House home building',
    'tree': 'Tree plant nature',
    'book': 'Book reading pages',
    'chair': 'Chair furniture seating',
    'table': 'Table furniture wooden',
    'phone': 'Mobile phone smartphone',
    'umbrella': 'Umbrella rain parasol',
    'bicycle': 'Bicycle bike cycling',
}

# Bollywood actors
bollywood = {
    'srk': 'Shah Rukh Khan Bollywood actor',
    'amitabh': 'Amitabh Bachchan Bollywood',
    'salman': 'Salman Khan Bollywood actor',
    'deepika': 'Deepika Padukone Bollywood actress',
    'hrithik': 'Hrithik Roshan Bollywood actor',
    'priyanka': 'Priyanka Chopra Bollywood actress',
    'aamir': 'Aamir Khan Bollywood actor',
    'alia': 'Alia Bhatt Bollywood actress',
    'ranbir': 'Ranbir Kapoor Bollywood actor',
    'katrina': 'Katrina Kaif Bollywood actress',
}

def get_images_from_bing(search_query, num_images=5):
    """
    Fetch image URLs from Bing Image Search
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        
        # Bing Image Search URL
        search_url = f"https://www.bing.com/images/search?q={quote(search_query)}&count={num_images}"
        
        response = requests.get(search_url, headers=headers, timeout=15)
        
        # Extract image URLs from the response
        img_urls = re.findall(r'murl["\']?:["\']?([^"\']*\.(?:jpg|jpeg|png|gif|webp))', response.text, re.IGNORECASE)
        
        # Also try to find URLs in a different format
        if not img_urls:
            img_urls = re.findall(r'"url":"([^"]*\.(?:jpg|jpeg|png|gif|webp)[^"]*)"', response.text, re.IGNORECASE)
        
        return img_urls[:num_images]
    except Exception as e:
        print(f"  Error fetching from Bing: {e}")
        return []

def download_image(url, save_path, timeout=15):
    """
    Download image from URL and save it
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.bing.com/',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        
        if response.status_code == 200:
            # Try to open and verify it's a valid image
            img = Image.open(BytesIO(response.content))
            
            # Convert to RGB if needed (to handle RGBA, etc.)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            img.save(save_path, 'PNG')
            return True
    except Exception as e:
        return False
    
    return False

def search_and_download(search_query, save_path, max_retries=3):
    """
    Search for an image and download the first valid result
    """
    for attempt in range(max_retries):
        try:
            # Get image URLs from Bing
            urls = get_images_from_bing(search_query, num_images=15)
            
            if not urls:
                if attempt == max_retries - 1:
                    print(f"  No URLs found")
                return False if attempt == max_retries - 1 else None
            
            # Try each URL until one works
            for url in urls:
                if download_image(url, save_path):
                    return True
            
            # If no URL worked, wait and try again
            if attempt < max_retries - 1:
                time.sleep(2)
        
        except Exception as e:
            print(f"  Error in attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    
    return False

# Download animals
print("=" * 60)
print("Downloading ANIMAL images from Bing Image Search...")
print("=" * 60)
for filename, search_query in animals.items():
    save_path = os.path.join(animals_dir, f"{filename}.png")
    print(f"\n[{filename.upper()}] Searching for: {search_query}")
    
    if os.path.exists(save_path):
        file_size = os.path.getsize(save_path) / 1024
        print(f"  ✓ Already exists ({file_size:.1f} KB)")
    else:
        print(f"  Downloading...", end="", flush=True)
        if search_and_download(search_query, save_path):
            file_size = os.path.getsize(save_path) / 1024
            print(f" ✓ ({file_size:.1f} KB)")
        else:
            print(f" ✗ Failed")
    
    time.sleep(1)

# Download things
print("\n" + "=" * 60)
print("Downloading THING images from Bing Image Search...")
print("=" * 60)
for filename, search_query in things.items():
    save_path = os.path.join(things_dir, f"{filename}.png")
    print(f"\n[{filename.upper()}] Searching for: {search_query}")
    
    if os.path.exists(save_path):
        file_size = os.path.getsize(save_path) / 1024
        print(f"  ✓ Already exists ({file_size:.1f} KB)")
    else:
        print(f"  Downloading...", end="", flush=True)
        if search_and_download(search_query, save_path):
            file_size = os.path.getsize(save_path) / 1024
            print(f" ✓ ({file_size:.1f} KB)")
        else:
            print(f" ✗ Failed")
    
    time.sleep(1)

# Download bollywood actors
print("\n" + "=" * 60)
print("Downloading BOLLYWOOD images from Bing Image Search...")
print("=" * 60)
for filename, search_query in bollywood.items():
    save_path = os.path.join(bollywood_dir, f"{filename}.png")
    print(f"\n[{filename.upper()}] Searching for: {search_query}")
    
    if os.path.exists(save_path):
        file_size = os.path.getsize(save_path) / 1024
        print(f"  ✓ Already exists ({file_size:.1f} KB)")
    else:
        print(f"  Downloading...", end="", flush=True)
        if search_and_download(search_query, save_path):
            file_size = os.path.getsize(save_path) / 1024
            print(f" ✓ ({file_size:.1f} KB)")
        else:
            print(f" ✗ Failed")
    
    time.sleep(1)

print("\n" + "=" * 60)
print("Download complete!")
print("=" * 60)
print(f"\n✓ Animals: {len(os.listdir(animals_dir))}/10")
print(f"✓ Things: {len(os.listdir(things_dir))}/10")
print(f"✓ Bollywood: {len(os.listdir(bollywood_dir))}/10")
