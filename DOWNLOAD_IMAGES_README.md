# 🖼️ Smart Image Downloader Guide

## Overview
The `download_images_smart.py` script allows you to automatically download images from Bing Image Search for your game categories.

## Features ✨

✅ **Smart downloading** - Only downloads for categories you specify
✅ **Duplicate prevention** - Skips images that already exist
✅ **Error handling** - Continues downloading even if some fail
✅ **Detailed reporting** - Shows what was downloaded, skipped, and failed
✅ **No overwrites** - Won't replace existing images by default
✅ **Category validation** - Checks if category exists before downloading

## How to Use 🚀

### Step 1: Run the Script
```bash
.\.venv\Scripts\python.exe .\download_images_smart.py
```

### Step 2: Select Categories
When prompted, enter the categories you want to download for:
```
Enter category names: fruits,professions,vehicles
```

Available categories:
- `animals`
- `things`
- `bollywood`
- `food`
- `sports`
- `monuments`

### Step 3: Choose Re-download Option
```
Do you want to re-download images that already exist? (y/n)
```
- Type `y` to re-download all images (even if they exist)
- Type `n` to skip existing images (recommended)

### Step 4: Wait for Download
The script will:
1. Check if each image already exists
2. Skip existing images ⏭️
3. Download missing images ✅
4. Report any failures ❌

## Output Example 📊

```
============================================================
📥 Downloading images for: FRUITS
============================================================
Total items to process: 10

  [1/10] ✅ DONE: Mango
  [2/10] ⏭️  SKIP: Banana (already exists)
  [3/10] ✅ DONE: Papaya
  [4/10] ❌ FAILED: Pomegranate
  [5/10] ✅ DONE: Coconut
  ...

============================================================
📊 DOWNLOAD SUMMARY
============================================================

📂 FRUITS
   Total items: 10
   ✅ Downloaded: 7
   ⏭️  Skipped (already exist): 2
   ❌ Failed: 1
   Failed items: pomegranate

============================================================
🎯 OVERALL STATISTICS
============================================================
Total categories processed: 1
Total items: 10
✅ Successfully downloaded: 7
⏭️  Already existed (skipped): 2
❌ Failed to download: 1
============================================================
```

## Multiple Categories 🎯

You can download for multiple categories at once:
```
Enter category names: fruits,professions,vehicles
```

## Tips & Tricks 💡

1. **Network:** Make sure you have a stable internet connection
2. **Speed:** First download will be slower, subsequent runs will be faster (skips existing)
3. **Failures:** If an image fails, you can run the script again - it will retry
4. **Format:** Images are automatically saved in appropriate formats (jpg, png)
5. **Organization:** Images are stored in `images/[category_name]/` folders

## First Time Setup

If you need to add a new category:
1. Add it to `categories.json` with item names
2. Run the downloader script
3. The script will create the category folder and download images

## Troubleshooting 🔧

**Q: Script stuck or slow?**
- A: Check your internet connection, it might be downloading large images

**Q: Images not downloading?**
- A: Try running again, some items might just not be available

**Q: Want to re-download everything?**
- A: Choose `y` when asked about re-downloading

**Q: Script doesn't find the package?**
- A: Make sure virtual environment is activated:
  ```bash
  .\.venv\Scripts\Activate.ps1
  ```

## Creating New Categories 📝

To add a new category for downloading:

1. **Add to categories.json:**
```json
"fruits": [
    { "image": "images/fruits/mango.jpg", "name": "Mango" },
    { "image": "images/fruits/banana.jpg", "name": "Banana" },
    ...
]
```

2. **Run the downloader:**
```bash
.\.venv\Scripts\python.exe .\download_images_smart.py
```

3. **Enter the category name:** `fruits`

The script will create the folder and download all images!

---

**Happy downloading! 🎮📸**
