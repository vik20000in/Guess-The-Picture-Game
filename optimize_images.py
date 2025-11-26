"""
Image Optimization Script
Compresses and optimizes images while maintaining quality
"""
import os
from pathlib import Path
from PIL import Image

def get_folder_size(folder_path):
    """Calculate total size of folder in MB"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size / (1024 * 1024)  # Convert to MB

def optimize_image(image_path, max_width=800, quality=85):
    """
    Optimize a single image:
    - Resize if larger than max_width
    - Compress with specified quality
    - Convert to progressive JPG for faster loading
    """
    try:
        img = Image.open(image_path)
        
        # Convert RGBA to RGB if needed (for JPG compatibility)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        
        # Get original size
        original_size = os.path.getsize(image_path)
        
        # Resize if image is too large
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Save with optimization
        img.save(
            image_path,
            'JPEG',
            quality=quality,
            optimize=True,
            progressive=True
        )
        
        new_size = os.path.getsize(image_path)
        saved = original_size - new_size
        
        return {
            'path': image_path,
            'original_size': original_size,
            'new_size': new_size,
            'saved': saved,
            'success': True
        }
    
    except Exception as e:
        return {
            'path': image_path,
            'success': False,
            'error': str(e)
        }

def optimize_images_in_folder(base_folder='images', max_width=800, quality=85):
    """
    Optimize all images in the images folder
    """
    base_path = Path(base_folder)
    
    if not base_path.exists():
        print(f"Error: {base_folder} folder not found")
        return
    
    # Calculate initial size
    initial_size = get_folder_size(base_path)
    print(f"Initial folder size: {initial_size:.2f} MB")
    print(f"\nOptimizing images (max_width={max_width}px, quality={quality}%)...")
    print("-" * 70)
    
    # Find all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(base_path.rglob(f'*{ext}'))
    
    total_images = len(image_files)
    total_saved = 0
    successful = 0
    failed = 0
    
    for i, img_path in enumerate(image_files, 1):
        result = optimize_image(str(img_path), max_width=max_width, quality=quality)
        
        if result['success']:
            successful += 1
            total_saved += result['saved']
            saved_kb = result['saved'] / 1024
            reduction = (result['saved'] / result['original_size'] * 100) if result['original_size'] > 0 else 0
            
            print(f"[{i}/{total_images}] {img_path.name}: "
                  f"Saved {saved_kb:.1f} KB ({reduction:.1f}% reduction)")
        else:
            failed += 1
            print(f"[{i}/{total_images}] {img_path.name}: FAILED - {result['error']}")
    
    # Calculate final size
    final_size = get_folder_size(base_path)
    total_saved_mb = initial_size - final_size
    
    print("-" * 70)
    print(f"\nOptimization Complete!")
    print(f"Processed: {total_images} images")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"\nInitial size: {initial_size:.2f} MB")
    print(f"Final size: {final_size:.2f} MB")
    print(f"Total saved: {total_saved_mb:.2f} MB ({(total_saved_mb/initial_size*100):.1f}% reduction)")

if __name__ == '__main__':
    import sys
    
    # Parse command line arguments
    max_width = 800  # Default max width
    quality = 85     # Default quality
    
    if len(sys.argv) > 1:
        max_width = int(sys.argv[1])
    if len(sys.argv) > 2:
        quality = int(sys.argv[2])
    
    print("=" * 70)
    print("IMAGE OPTIMIZATION TOOL")
    print("=" * 70)
    print(f"Settings: Max Width = {max_width}px, Quality = {quality}%")
    print()
    
    optimize_images_in_folder(max_width=max_width, quality=quality)
