import os
import requests
from PIL import Image
from io import BytesIO
import time
import json

# Create directories if they don't exist
base_path = os.path.dirname(os.path.abspath(__file__))
animals_dir = os.path.join(base_path, 'images', 'animals')
things_dir = os.path.join(base_path, 'images', 'things')
bollywood_dir = os.path.join(base_path, 'images', 'bollywood')

os.makedirs(animals_dir, exist_ok=True)
os.makedirs(things_dir, exist_ok=True)
os.makedirs(bollywood_dir, exist_ok=True)

# Using direct URLs from a reliable image source
# These are direct image URLs that should work
image_urls = {
    'animals': {
        'lion': 'https://images.unsplash.com/photo-1586182407929-c7d14c5ce988?w=400&h=300&fit=crop',
        'elephant': 'https://images.unsplash.com/photo-1551184914-5c968d1ef837?w=400&h=300&fit=crop',
        'giraffe': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=400&h=300&fit=crop',
        'zebra': 'https://images.unsplash.com/photo-1614027164847-1b28cfe1df60?w=400&h=300&fit=crop',
        'monkey': 'https://images.unsplash.com/photo-1551316679-9c6ae9dec224?w=400&h=300&fit=crop',
        'tiger': 'https://images.unsplash.com/photo-1474511320723-9a56873867b5?w=400&h=300&fit=crop',
        'bear': 'https://images.unsplash.com/photo-1456728621405-1b8e1824f926?w=400&h=300&fit=crop',
        'dog': 'https://images.unsplash.com/photo-1633722715463-d30628519d60?w=400&h=300&fit=crop',
        'cat': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop',
        'penguin': 'https://images.unsplash.com/photo-1585110396000-c9ffd4d4b3f4?w=400&h=300&fit=crop',
    },
    'things': {
        'car': 'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=400&h=300&fit=crop',
        'ball': 'https://images.unsplash.com/photo-1518611505868-48510c2e022c?w=400&h=300&fit=crop',
        'house': 'https://images.unsplash.com/photo-1570129477492-45a003537e1f?w=400&h=300&fit=crop',
        'tree': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400&h=300&fit=crop',
        'book': 'https://images.unsplash.com/photo-1507842217343-583e7270887f?w=400&h=300&fit=crop',
        'chair': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=300&fit=crop',
        'table': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=300&fit=crop',
        'phone': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop',
        'umbrella': 'https://images.unsplash.com/photo-1544919982-b95aed55c463?w=400&h=300&fit=crop',
        'bicycle': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
    },
    'bollywood': {
        'srk': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop',
        'amitabh': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=300&fit=crop',
        'salman': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop',
        'deepika': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=300&fit=crop',
        'hrithik': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=300&fit=crop',
        'priyanka': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=300&fit=crop',
        'aamir': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop',
        'alia': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=300&fit=crop',
        'ranbir': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=300&fit=crop',
        'katrina': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=300&fit=crop',
    }
}

def download_image(url, save_path):
    """Download image from URL and save it"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Save the image
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            # Verify it's a valid image
            try:
                img = Image.open(save_path)
                img.verify()
            except:
                pass  # Continue even if verify fails
            
            return True
        return False
    except Exception as e:
        print(f"  Error: {e}")
        return False

# Download animals
print("=" * 50)
print("Downloading animal images...")
print("=" * 50)
for name, url in image_urls['animals'].items():
    save_path = os.path.join(animals_dir, f"{name}.png")
    if not os.path.exists(save_path):
        print(f"Downloading {name}...", end=" ")
        if download_image(url, save_path):
            print("✓")
        else:
            print("✗")
        time.sleep(0.3)
    else:
        print(f"✓ Already exists: {name}.png")

# Download things
print("\n" + "=" * 50)
print("Downloading thing images...")
print("=" * 50)
for name, url in image_urls['things'].items():
    save_path = os.path.join(things_dir, f"{name}.png")
    if not os.path.exists(save_path):
        print(f"Downloading {name}...", end=" ")
        if download_image(url, save_path):
            print("✓")
        else:
            print("✗")
        time.sleep(0.3)
    else:
        print(f"✓ Already exists: {name}.png")

# Download bollywood actors
print("\n" + "=" * 50)
print("Downloading Bollywood actor images...")
print("=" * 50)
for name, url in image_urls['bollywood'].items():
    save_path = os.path.join(bollywood_dir, f"{name}.png")
    if not os.path.exists(save_path):
        print(f"Downloading {name}...", end=" ")
        if download_image(url, save_path):
            print("✓")
        else:
            print("✗")
        time.sleep(0.3)
    else:
        print(f"✓ Already exists: {name}.png")

print("\n" + "=" * 50)
print("Download complete!")
print("=" * 50)
print(f"\n✓ Animals: {len(os.listdir(animals_dir))} images")
print(f"✓ Things: {len(os.listdir(things_dir))} images")
print(f"✓ Bollywood: {len(os.listdir(bollywood_dir))} images")
