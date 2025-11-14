import os
import requests
from PIL import Image
from io import BytesIO
import time
import json
from urllib.parse import quote

# Create directories if they don't exist
base_path = os.path.dirname(os.path.abspath(__file__))
animals_dir = os.path.join(base_path, 'images', 'animals')
things_dir = os.path.join(base_path, 'images', 'things')
bollywood_dir = os.path.join(base_path, 'images', 'bollywood')

os.makedirs(animals_dir, exist_ok=True)
os.makedirs(things_dir, exist_ok=True)
os.makedirs(bollywood_dir, exist_ok=True)

# Image URLs from reliable sources (Wikimedia Commons, Free Stock Photos, etc.)
image_urls = {
    'animals': {
        'lion': [
            'https://images.unsplash.com/photo-1586182407929-c7d14c5ce988?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1577557996664-20d192d3b331?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=600&h=400&fit=crop',
        ],
        'elephant': [
            'https://images.unsplash.com/photo-1564349957253-0f14d8e23efc?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1551184914-5c968d1ef837?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1589956154285-aa2a2f3a0e36?w=600&h=400&fit=crop',
            'https://images.pexels.com/photos/66898/elephant-cub-elephant-baby-young-66898.jpeg',
            'https://images.pexels.com/photos/51381/elephant-cub-tusk-wildlife-51381.jpeg',
            'https://cdn.pixabay.com/photo/2018/04/03/14/31/african-elephant-3285959_960_720.jpg',
        ],
        'giraffe': [
            'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1578206408950-2b89b2a94f6a?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1461611876519-a2b134e6fb89?w=600&h=400&fit=crop',
        ],
        'zebra': [
            'https://images.unsplash.com/photo-1614027164847-1b28cfe1df60?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1557050543-4d5ec3c58898?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1590859669661-fcf85e859868?w=600&h=400&fit=crop',
        ],
        'monkey': [
            'https://images.unsplash.com/photo-1551316679-9c6ae9dec224?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1551082641-a8ddf3b94fbe?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1550932256-4f3aa07f6e4a?w=600&h=400&fit=crop',
        ],
        'tiger': [
            'https://images.unsplash.com/photo-1474511320723-9a56873867b5?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1618826411640-d6df44dd3f7a?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1520763185298-1b434c919eba?w=600&h=400&fit=crop',
        ],
        'bear': [
            'https://images.unsplash.com/photo-1456728621405-1b8e1824f926?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1486688333404-e81f27f7a0c2?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1540573133985-87b6da8df204?w=600&h=400&fit=crop',
            'https://images.pexels.com/photos/33537/child-children-girl-happy.jpeg',
            'https://images.pexels.com/photos/54216/panda-bear-giant-panda-bear-cub-54216.jpeg',
            'https://cdn.pixabay.com/photo/2016/02/18/16/27/bear-1207919_960_720.jpg',
        ],
        'dog': [
            'https://images.unsplash.com/photo-1633722715463-d30628519d60?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1633627962476-1b12fa5f27f7?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1615751072497-5f5169febe17?w=600&h=400&fit=crop',
        ],
        'cat': [
            'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1513245543132-31f0213d31d0?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1519052537078-e6302a4968d4?w=600&h=400&fit=crop',
        ],
        'penguin': [
            'https://images.unsplash.com/photo-1585110396000-c9ffd4d4b3f4?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1551819563-3f2c0f6b8228?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1606567595334-d72962b592ca?w=600&h=400&fit=crop',
            'https://images.pexels.com/photos/1387174/pexels-photo-1387174.jpeg',
            'https://images.pexels.com/photos/2317904/pexels-photo-2317904.jpeg',
        ],
    },
    'things': {
        'car': [
            'https://images.unsplash.com/photo-1552820728-8ac41f1ce891?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1619405399517-d4620f4a9ad9?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1493238792313-cd271419b14f?w=600&h=400&fit=crop',
            'https://images.pexels.com/photos/163995/pexels-photo-163995.jpeg',
            'https://images.pexels.com/photos/97079/pexels-photo-97079.jpeg',
        ],
        'ball': [
            'https://images.unsplash.com/photo-1518611505868-48510c2e022c?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1624526267942-ab67cb1ef672?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1599574924326-db46fd09020d?w=600&h=400&fit=crop',
            'https://images.pexels.com/photos/159840/ball-pink-equipment-childhood-159840.jpeg',
            'https://images.pexels.com/photos/50578/soccer-ball-sport-ball-sphere-50578.jpeg',
            'https://cdn.pixabay.com/photo/2016/04/02/14/12/ball-1303210_960_720.jpg',
        ],
        'house': [
            'https://images.unsplash.com/photo-1570129477492-45a003537e1f?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1575507175277-f6d50b62ab13?w=600&h=400&fit=crop',
        ],
        'tree': [
            'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&h=400&fit=crop',
        ],
        'book': [
            'https://images.unsplash.com/photo-1507842217343-583e7270887f?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1507842217343-583e7270887f?w=600&h=400&fit=crop',
        ],
        'chair': [
            'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1532159361995-fca3dca89f97?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=600&h=400&fit=crop',
        ],
        'table': [
            'https://images.unsplash.com/photo-1533090161392-a8255ba84241?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600&h=400&fit=crop',
        ],
        'phone': [
            'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1511707267537-b85faf00021e?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=600&h=400&fit=crop',
        ],
        'umbrella': [
            'https://images.unsplash.com/photo-1544919982-b95aed55c463?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1559657261-7ac96776944a?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&h=400&fit=crop',
        ],
        'bicycle': [
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=600&h=400&fit=crop',
        ],
    },
    'bollywood': {
        'srk': [
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=600&h=400&fit=crop',
        ],
        'amitabh': [
            'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=600&h=400&fit=crop',
        ],
        'salman': [
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=600&h=400&fit=crop',
        ],
        'deepika': [
            'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=600&h=400&fit=crop',
        ],
        'hrithik': [
            'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=600&h=400&fit=crop',
        ],
        'priyanka': [
            'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=600&h=400&fit=crop',
        ],
        'aamir': [
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=600&h=400&fit=crop',
        ],
        'alia': [
            'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=600&h=400&fit=crop',
        ],
        'ranbir': [
            'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=600&h=400&fit=crop',
        ],
        'katrina': [
            'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
            'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=600&h=400&fit=crop',
        ],
    }
}

def download_image(url, save_path, timeout=15):
    """
    Download image from URL and save it
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        
        if response.status_code == 200:
            # Try to open and verify it's a valid image
            img = Image.open(BytesIO(response.content))
            
            # Convert to RGB if needed (to handle RGBA, LA, P modes)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            img.save(save_path, 'PNG')
            return True
    except Exception as e:
        return False
    
    return False

def search_and_download(search_query, urls_list, save_path, max_retries=2):
    """
    Try downloading from provided URL list
    """
    for attempt in range(max_retries):
        try:
            # Try each URL until one works
            for url in urls_list:
                if download_image(url, save_path):
                    return True
            
            # If no URL worked, wait and try again
            if attempt < max_retries - 1:
                time.sleep(1)
        
        except Exception as e:
            print(f"  Error in attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
    
    return False

# Download animals
print("=" * 60)
print("Downloading ANIMAL images...")
print("=" * 60)
for filename, urls_list in image_urls['animals'].items():
    save_path = os.path.join(animals_dir, f"{filename}.png")
    print(f"\n[{filename.upper()}]", end=" ")
    
    if os.path.exists(save_path):
        file_size = os.path.getsize(save_path) / 1024
        print(f"✓ Already exists ({file_size:.1f} KB)")
    else:
        print(f"Downloading...", end="", flush=True)
        if search_and_download(filename, urls_list, save_path):
            file_size = os.path.getsize(save_path) / 1024
            print(f" ✓ ({file_size:.1f} KB)")
        else:
            print(f" ✗ Failed")
    
    time.sleep(0.5)

# Download things
print("\n" + "=" * 60)
print("Downloading THING images...")
print("=" * 60)
for filename, urls_list in image_urls['things'].items():
    save_path = os.path.join(things_dir, f"{filename}.png")
    print(f"\n[{filename.upper()}]", end=" ")
    
    if os.path.exists(save_path):
        file_size = os.path.getsize(save_path) / 1024
        print(f"✓ Already exists ({file_size:.1f} KB)")
    else:
        print(f"Downloading...", end="", flush=True)
        if search_and_download(filename, urls_list, save_path):
            file_size = os.path.getsize(save_path) / 1024
            print(f" ✓ ({file_size:.1f} KB)")
        else:
            print(f" ✗ Failed")
    
    time.sleep(0.5)

# Download bollywood actors
print("\n" + "=" * 60)
print("Downloading BOLLYWOOD images...")
print("=" * 60)
for filename, urls_list in image_urls['bollywood'].items():
    save_path = os.path.join(bollywood_dir, f"{filename}.png")
    print(f"\n[{filename.upper()}]", end=" ")
    
    if os.path.exists(save_path):
        file_size = os.path.getsize(save_path) / 1024
        print(f"✓ Already exists ({file_size:.1f} KB)")
    else:
        print(f"Downloading...", end="", flush=True)
        if search_and_download(filename, urls_list, save_path):
            file_size = os.path.getsize(save_path) / 1024
            print(f" ✓ ({file_size:.1f} KB)")
        else:
            print(f" ✗ Failed")
    
    time.sleep(0.5)

print("\n" + "=" * 60)
print("Download complete!")
print("=" * 60)
print(f"\n✓ Animals: {len(os.listdir(animals_dir))}/10")
print(f"✓ Things: {len(os.listdir(things_dir))}/10")
print(f"✓ Bollywood: {len(os.listdir(bollywood_dir))}/10")
