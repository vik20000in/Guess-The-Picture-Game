"""
Simple Image Downloader using free APIs
Downloads images for game categories from multiple sources
"""
import json
import os
import requests
from pathlib import Path
import time

CATEGORIES_FILE = 'categories.json'
IMAGES_BASE_DIR = 'images'
TIMEOUT = 30

def load_categories():
    """Load categories from JSON file"""
    with open(CATEGORIES_FILE, 'r') as f:
        return json.load(f)

def download_image_from_apis(search_term, output_path, max_retries=3):
    """
    Download image using multiple free APIs in order:
    1. Unsplash (requires no auth for limited requests)
    2. Pexels (free stock photos)
    3. Pixabay (free images)
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Try Unsplash API (no auth needed for search)
    try:
        response = requests.get(
            f"https://api.unsplash.com/search/photos",
            params={
                'query': search_term,
                'per_page': 1,
                'order_by': 'relevant'
            },
            timeout=TIMEOUT,
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                image_url = data['results'][0]['urls']['regular']
                img_response = requests.get(image_url, timeout=TIMEOUT, headers=headers)
                
                if img_response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    return True
    except Exception as e:
        pass
    
    # Try Pexels API
    try:
        response = requests.get(
            f"https://api.pexels.com/v1/search",
            params={
                'query': search_term,
                'per_page': 1
            },
            timeout=TIMEOUT,
            headers={'Authorization': '563492ad6f9170000100000190f9e99f23cf4fb7a6f5c6ab0f67e0ee'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('photos'):
                image_url = data['photos'][0]['src']['medium']
                img_response = requests.get(image_url, timeout=TIMEOUT, headers=headers)
                
                if img_response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    return True
    except Exception as e:
        pass
    
    # Try Pixabay API
    try:
        response = requests.get(
            f"https://pixabay.com/api/",
            params={
                'key': '43537080-5e0a859a0db33be1f0df5a22a',
                'q': search_term,
                'per_page': 1,
                'image_type': 'photo',
                'order': 'popular'
            },
            timeout=TIMEOUT,
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('hits'):
                image_url = data['hits'][0]['webformatURL']
                img_response = requests.get(image_url, timeout=TIMEOUT, headers=headers)
                
                if img_response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    return True
    except Exception as e:
        pass
    
    return False

def download_images_for_category(category_name, categories_data, force_redownload=False):
    """Download images for a specific category"""
    if category_name not in categories_data:
        print(f"\n❌ Category '{category_name}' not found in categories.json")
        return None
    
    items = categories_data[category_name]
    category_dir = os.path.join(IMAGES_BASE_DIR, category_name)
    
    os.makedirs(category_dir, exist_ok=True)
    
    stats = {
        'category': category_name,
        'total': len(items),
        'downloaded': 0,
        'skipped': 0,
        'failed': [],
        'skipped_list': []
    }
    
    print(f"\n{'='*60}")
    print(f"📥 Downloading images for: {category_name.upper()}")
    print(f"{'='*60}")
    print(f"Total items to process: {len(items)}\n")
    
    for idx, item in enumerate(items, 1):
        item_name = item['name']
        image_path = item['image']
        filename = os.path.basename(image_path)
        full_path = os.path.join(category_dir, filename)
        
        if os.path.exists(full_path) and not force_redownload:
            print(f"  [{idx:2d}/{len(items)}] ⏭️  SKIP: {item_name:<20} (already exists)")
            stats['skipped'] += 1
            stats['skipped_list'].append(item_name)
            continue
        
        print(f"  [{idx:2d}/{len(items)}] 🔄 Downloading: {item_name:<20}...", end=" ", flush=True)
        try:
            success = download_image_from_apis(item_name, full_path)
            if success:
                print("✅ DONE")
                stats['downloaded'] += 1
            else:
                print("❌ FAILED")
                stats['failed'].append(item_name)
        except Exception as e:
            print(f"❌ ERROR")
            stats['failed'].append(item_name)
        
        time.sleep(0.3)  # Small delay between requests
    
    return stats

def print_statistics(all_stats):
    """Print comprehensive download statistics"""
    total_downloaded = sum(s['downloaded'] for s in all_stats)
    total_skipped = sum(s['skipped'] for s in all_stats)
    total_items = sum(s['total'] for s in all_stats)
    total_failed = sum(len(s['failed']) for s in all_stats)
    
    print(f"\n{'='*60}")
    print("📊 DOWNLOAD SUMMARY")
    print(f"{'='*60}\n")
    
    for stats in all_stats:
        print(f"📂 {stats['category'].upper()}")
        print(f"   Total items: {stats['total']}")
        print(f"   ✅ Downloaded: {stats['downloaded']}")
        print(f"   ⏭️  Skipped (already exist): {stats['skipped']}")
        print(f"   ❌ Failed: {len(stats['failed'])}")
        
        if stats['failed']:
            print(f"   Failed items: {', '.join(stats['failed'][:5])}", end="")
            if len(stats['failed']) > 5:
                print(f" ... and {len(stats['failed']) - 5} more")
            else:
                print()
        print()
    
    print(f"{'='*60}")
    print("🎯 OVERALL STATISTICS")
    print(f"{'='*60}")
    print(f"Total categories processed: {len(all_stats)}")
    print(f"Total items: {total_items}")
    print(f"✅ Successfully downloaded: {total_downloaded}")
    print(f"⏭️  Already existed (skipped): {total_skipped}")
    print(f"❌ Failed to download: {total_failed}")
    print(f"{'='*60}\n")

def main():
    """Main function"""
    print("\n🎮 SMART IMAGE DOWNLOADER FOR GUESS THE PICTURE GAME\n")
    
    try:
        categories_data = load_categories()
    except FileNotFoundError:
        print(f"❌ Error: {CATEGORIES_FILE} not found!")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: {CATEGORIES_FILE} is not valid JSON!")
        return
    
    print("Available categories:")
    for i, cat in enumerate(categories_data.keys(), 1):
        count = len(categories_data[cat])
        print(f"  {i}. {cat} ({count} items)")
    
    print("\n" + "="*60)
    print("Enter the categories you want to download for (comma-separated)")
    print("Example: fruits,professions,vehicles")
    print("="*60 + "\n")
    
    user_input = input("Enter category names: ").strip()
    
    if not user_input:
        print("\nNo categories selected. Exiting.")
        return
    
    requested_categories = [cat.strip().lower() for cat in user_input.split(',')]
    
    valid_categories = []
    for cat in requested_categories:
        if cat in categories_data:
            valid_categories.append(cat)
        else:
            print(f"⚠️  Warning: Category '{cat}' not found, skipping...")
    
    if not valid_categories:
        print("❌ No valid categories selected. Exiting.")
        return
    
    print(f"\n✅ Selected categories: {', '.join(valid_categories)}")
    
    print("\nDo you want to re-download images that already exist? (y/n)")
    response = input("Enter choice: ").strip().lower()
    force_redownload = response == 'y'
    
    if force_redownload:
        print("⚠️  Will re-download existing images")
    else:
        print("✅ Will skip existing images")
    
    all_stats = []
    for category in valid_categories:
        stats = download_images_for_category(category, categories_data, force_redownload)
        if stats:
            all_stats.append(stats)
    
    if all_stats:
        print_statistics(all_stats)

if __name__ == "__main__":
    main()
