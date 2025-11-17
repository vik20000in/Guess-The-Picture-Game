import os
import requests
from PIL import Image
from io import BytesIO
import time

# Create directories if they don't exist
base_path = os.path.dirname(os.path.abspath(__file__))
fruits_dir = os.path.join(base_path, 'images', 'fruits')

os.makedirs(fruits_dir, exist_ok=True)

# Fruit names and URLs from reliable sources
image_urls = {
    'mango': [
        'https://images.unsplash.com/photo-1553279768-865a24cda3ca?w=600&h=400&fit=crop',
        'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/4551832/pexels-photo-4551832.jpeg',
    ],
    'banana': [
        'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=600&h=400&fit=crop',
        'https://images.unsplash.com/photo-1528741891733-c63adf4c0d33?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632656/pexels-photo-5632656.jpeg',
    ],
    'apple': [
        'https://images.unsplash.com/photo-1560806674-9a308e0acf4e?w=600&h=400&fit=crop',
        'https://images.unsplash.com/photo-1629636716969-14ae9b4f88d9?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/102104/pexels-photo-102104.jpeg',
    ],
    'papaya': [
        'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632664/pexels-photo-5632664.jpeg',
        'https://cdn.pixabay.com/photo/2020/07/26/20/32/papaya-5438118_960_720.jpg',
    ],
    'coconut': [
        'https://images.unsplash.com/photo-1585686914537-c5b16ef39d7d?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/2909035/pexels-photo-2909035.jpeg',
        'https://cdn.pixabay.com/photo/2016/08/15/04/23/coconut-1594738_960_720.jpg',
    ],
    'guava': [
        'https://cdn.pixabay.com/photo/2019/08/29/15/16/guava-4439256_960_720.jpg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/4551832/pexels-photo-4551832.jpeg',
    ],
    'pomegranate': [
        'https://cdn.pixabay.com/photo/2020/06/06/21/33/pomegranate-5269408_960_720.jpg',
        'https://images.pexels.com/photos/5632679/pexels-photo-5632679.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'watermelon': [
        'https://images.unsplash.com/photo-1582979604563-430f63602d4b?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/2105285/pexels-photo-2105285.jpeg',
        'https://cdn.pixabay.com/photo/2014/12/21/23/50/watermelon-577447_960_720.jpg',
    ],
    'pineapple': [
        'https://cdn.pixabay.com/photo/2016/08/15/04/22/pineapple-1595523_960_720.jpg',
        'https://images.pexels.com/photos/2291129/pexels-photo-2291129.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'orange': [
        'https://cdn.pixabay.com/photo/2018/02/03/00/37/orange-3127334_960_720.jpg',
        'https://images.pexels.com/photos/5632653/pexels-photo-5632653.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'lemon': [
        'https://cdn.pixabay.com/photo/2014/12/21/23/45/lemon-577441_960_720.jpg',
        'https://images.pexels.com/photos/6295/freshness-lemon-fruits-citrus.jpg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'lime': [
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632659/pexels-photo-5632659.jpeg',
        'https://cdn.pixabay.com/photo/2016/12/26/14/10/lime-1929092_960_720.jpg',
    ],
    'grapes': [
        'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632713/pexels-photo-5632713.jpeg',
        'https://cdn.pixabay.com/photo/2014/12/21/23/48/grapes-577445_960_720.jpg',
    ],
    'strawberry': [
        'https://images.unsplash.com/photo-1584708107257-3346f1be7dee?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632671/pexels-photo-5632671.jpeg',
        'https://cdn.pixabay.com/photo/2016/08/15/04/19/strawberry-1594622_960_720.jpg',
    ],
    'blueberry': [
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632700/pexels-photo-5632700.jpeg',
        'https://cdn.pixabay.com/photo/2016/08/15/04/17/blueberry-1594611_960_720.jpg',
    ],
    'raspberry': [
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632697/pexels-photo-5632697.jpeg',
        'https://cdn.pixabay.com/photo/2016/08/15/04/16/raspberry-1594608_960_720.jpg',
    ],
    'blackberry': [
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632703/pexels-photo-5632703.jpeg',
        'https://cdn.pixabay.com/photo/2016/08/15/04/15/blackberry-1594603_960_720.jpg',
    ],
    'kiwi': [
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632676/pexels-photo-5632676.jpeg',
        'https://cdn.pixabay.com/photo/2015/05/05/10/15/kiwi-755375_960_720.jpg',
    ],
    'peach': [
        'https://cdn.pixabay.com/photo/2018/05/17/03/36/peach-3408439_960_720.jpg',
        'https://images.pexels.com/photos/5632690/pexels-photo-5632690.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'pear': [
        'https://cdn.pixabay.com/photo/2014/12/21/23/49/pear-577450_960_720.jpg',
        'https://images.pexels.com/photos/5632693/pexels-photo-5632693.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'plum': [
        'https://cdn.pixabay.com/photo/2015/02/12/10/37/plum-633667_960_720.jpg',
        'https://images.pexels.com/photos/5632687/pexels-photo-5632687.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'apricot': [
        'https://cdn.pixabay.com/photo/2018/03/18/14/34/apricot-3235308_960_720.jpg',
        'https://images.pexels.com/photos/5632684/pexels-photo-5632684.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'cherry': [
        'https://cdn.pixabay.com/photo/2016/08/15/04/18/cherry-1594619_960_720.jpg',
        'https://images.pexels.com/photos/5632681/pexels-photo-5632681.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'dragon_fruit': [
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632706/pexels-photo-5632706.jpeg',
        'https://cdn.pixabay.com/photo/2018/06/12/18/21/dragon-fruit-3473627_960_720.jpg',
    ],
    'avocado': [
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/2351281/pexels-photo-2351281.jpeg',
        'https://cdn.pixabay.com/photo/2016/11/02/14/31/avocado-1791649_960_720.jpg',
    ],
    'passion_fruit': [
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632709/pexels-photo-5632709.jpeg',
        'https://cdn.pixabay.com/photo/2018/04/02/14/31/passion-fruit-3285887_960_720.jpg',
    ],
    'fig': [
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632712/pexels-photo-5632712.jpeg',
        'https://cdn.pixabay.com/photo/2017/04/12/17/23/fig-2223486_960_720.jpg',
    ],
    'date': [
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632723/pexels-photo-5632723.jpeg',
        'https://cdn.pixabay.com/photo/2016/12/15/15/55/date-palm-1909511_960_720.jpg',
    ],
    'litchi': [
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
        'https://images.pexels.com/photos/5632717/pexels-photo-5632717.jpeg',
        'https://cdn.pixabay.com/photo/2020/07/26/13/21/litchi-5437852_960_720.jpg',
    ],
    'longan': [
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
        'https://cdn.pixabay.com/photo/2020/07/26/13/22/longan-5437858_960_720.jpg',
        'https://images.pexels.com/photos/5632720/pexels-photo-5632720.jpeg',
    ],
    'jackfruit': [
        'https://cdn.pixabay.com/photo/2018/05/06/18/57/jackfruit-3380271_960_720.jpg',
        'https://images.pexels.com/photos/5632724/pexels-photo-5632724.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'custard_apple': [
        'https://cdn.pixabay.com/photo/2020/07/26/13/23/custard-apple-5437863_960_720.jpg',
        'https://images.pexels.com/photos/5632727/pexels-photo-5632727.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'sugar_cane': [
        'https://cdn.pixabay.com/photo/2018/06/12/18/22/sugar-cane-3473639_960_720.jpg',
        'https://images.pexels.com/photos/5632730/pexels-photo-5632730.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'carambola': [
        'https://cdn.pixabay.com/photo/2018/06/12/18/21/star-fruit-3473627_960_720.jpg',
        'https://images.pexels.com/photos/5632733/pexels-photo-5632733.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'mulberry': [
        'https://cdn.pixabay.com/photo/2018/04/02/14/31/mulberry-3285897_960_720.jpg',
        'https://images.pexels.com/photos/5632736/pexels-photo-5632736.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'tamarind': [
        'https://cdn.pixabay.com/photo/2020/07/26/13/24/tamarind-5437869_960_720.jpg',
        'https://images.pexels.com/photos/5632739/pexels-photo-5632739.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'grapefruit': [
        'https://cdn.pixabay.com/photo/2015/02/13/08/27/grapefruit-633695_960_720.jpg',
        'https://images.pexels.com/photos/5632742/pexels-photo-5632742.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'tangerine': [
        'https://cdn.pixabay.com/photo/2017/01/17/10/07/tangerine-1987207_960_720.jpg',
        'https://images.pexels.com/photos/5632745/pexels-photo-5632745.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'melon': [
        'https://cdn.pixabay.com/photo/2016/08/15/04/20/melon-1594630_960_720.jpg',
        'https://images.pexels.com/photos/2105285/pexels-photo-2105285.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
    'honeydew': [
        'https://cdn.pixabay.com/photo/2017/07/27/20/11/honeydew-melon-2545406_960_720.jpg',
        'https://images.pexels.com/photos/5632748/pexels-photo-5632748.jpeg',
        'https://images.unsplash.com/photo-1599599810694-b5ac4dd19453?w=600&h=400&fit=crop',
    ],
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
            
            img.save(save_path, 'JPEG')
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

# Download fruits
print("=" * 60)
print("Downloading FRUIT images...")
print("=" * 60)

successful = 0
failed = 0

for filename, urls_list in image_urls.items():
    save_path = os.path.join(fruits_dir, f"{filename}.jpg")
    print(f"\n[{filename.upper()}]", end=" ")
    
    if os.path.exists(save_path):
        file_size = os.path.getsize(save_path) / 1024
        print(f"✓ Already exists ({file_size:.1f} KB)")
        successful += 1
    else:
        print(f"Downloading...", end="", flush=True)
        if search_and_download(filename, urls_list, save_path):
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
    
    time.sleep(0.5)

print("\n" + "=" * 60)
print("Download complete!")
print("=" * 60)
total = len(image_urls)
print(f"\n✓ Successfully downloaded: {successful}/{total}")
if failed > 0:
    print(f"✗ Failed: {failed}/{total}")
