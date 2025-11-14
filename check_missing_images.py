import json
import os
from pathlib import Path

def check_missing_images():
    """Check which images referenced in categories.json are missing from the file system"""
    
    # Load categories.json
    with open('categories.json', 'r') as f:
        categories = json.load(f)
    
    missing_images = []
    found_images = []
    
    print("=" * 70)
    print("CHECKING IMAGE FILES FROM categories.json")
    print("=" * 70)
    
    # Check each category
    for category_name, items in categories.items():
        print(f"\n📁 Category: {category_name.upper()}")
        print(f"   Total items: {len(items)}")
        
        category_missing = []
        category_found = []
        
        for item in items:
            image_path = item['image']
            full_path = os.path.join(os.getcwd(), image_path)
            
            if os.path.exists(full_path):
                category_found.append(image_path)
                status = "✓"
            else:
                category_missing.append(image_path)
                missing_images.append({
                    'category': category_name,
                    'name': item['name'],
                    'path': image_path
                })
                status = "✗"
            
            print(f"   {status} {image_path:50} | {item['name']}")
        
        found_images.extend(category_found)
        
        # Summary for category
        print(f"   Found: {len(category_found)}/{len(items)}")
        if category_missing:
            print(f"   Missing: {len(category_missing)}/{len(items)}")
    
    # Overall summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total items in JSON: {len(found_images) + len(missing_images)}")
    print(f"✓ Images found: {len(found_images)}")
    print(f"✗ Images missing: {len(missing_images)}")
    
    if missing_images:
        print("\n" + "=" * 70)
        print("MISSING IMAGES DETAILS")
        print("=" * 70)
        for idx, missing in enumerate(missing_images, 1):
            print(f"\n{idx}. {missing['name']}")
            print(f"   Category: {missing['category']}")
            print(f"   Expected path: {missing['path']}")
    else:
        print("\n✓ All images are present!")
    
    print("\n" + "=" * 70)
    
    return missing_images

if __name__ == '__main__':
    missing = check_missing_images()
    
    # Optionally create a report file
    report_file = 'image_check_report.txt'
    with open(report_file, 'w') as f:
        f.write("IMAGE PRESENCE CHECK REPORT\n")
        f.write("=" * 70 + "\n\n")
        
        if missing:
            f.write(f"Total missing images: {len(missing)}\n\n")
            f.write("MISSING IMAGES:\n")
            for item in missing:
                f.write(f"- {item['name']} ({item['category']}): {item['path']}\n")
        else:
            f.write("✓ All images are present!\n")
    
    print(f"\n📄 Report saved to: {report_file}")
