# Image Verification with AI (FREE - No API Key Required!)

This tool uses FREE local AI models to automatically verify if images match their expected content. Everything runs on your computer - **no API keys, no costs, no cloud services required!**

## How It Works

Uses **BLIP** (Bootstrapping Language-Image Pre-training) - a state-of-the-art vision AI model from Salesforce:
- 🆓 **Completely FREE** - no API costs
- 🔒 **100% Private** - runs locally on your computer
- 📦 **Auto-downloads** - models are cached after first use
- 🚀 **Accurate** - uses advanced image captioning and visual Q&A

## Prerequisites

**Just Python!** That's it. No API keys needed.

## Setup

1. Install required libraries (first time only):
   ```powershell
   pip install transformers torch torchvision pillow
   ```

   The script will auto-install if needed. First run downloads AI models (~500MB) - they're cached for future use.

## Usage

### Quick Start

Simply run:
```powershell
python verify_images_with_ai.py
```

You'll be prompted with options:
1. **Verify all images** - Checks all images in all categories
2. **Verify a specific category** - Check just one category (e.g., "Vegetables", "Landmarks")
3. **Verify specific images** - Check individual images

### Programmatic Use

You can also import and use the functions in your own scripts:

```python
from verify_images_with_ai import verify_all_images, verify_single_category, verify_specific_images

# Verify all images (no API key needed!)
results, incorrect = verify_all_images()

# Verify just vegetables
results, incorrect = verify_single_category('Vegetables')

# Verify specific images
image_specs = [
    ('images/vegetables/tomato.jpg', 'Tomato', 'Vegetables'),
    ('images/birds/peacock.jpg', 'Peacock', 'Birds')
]
results = verify_specific_images(image_specs)
```

## How the AI Works

The BLIP model performs two types of analysis on each image:

1. **Image Captioning**: Generates a description of what's in the image
   - Example: "a red tomato on a white background"

2. **Visual Question Answering (VQA)**: Asks specific questions
   - "What is this?"
   - "Is this a [expected item]?"

The script then:
- Compares the AI's answers with the expected item name
- Calculates similarity scores
- Determines if the image is correct (threshold: 50% confidence)

## Output

### Console Output
The script provides real-time feedback:
- ✅ **Green checkmark** = Image is correct
- ❌ **Red X** = Image is incorrect or suspicious
- Each result shows confidence score (0.0 to 1.0)

### JSON Report
A detailed report is saved to `image_verification_report.json`:

```json
{
  "summary": {
    "total_checked": 100,
    "correct": 95,
    "incorrect": 5,
    "accuracy_percent": 95.0
  },
  "incorrect_images": [
    {
      "category": "Vegetables",
      "item": "Tomato",
      "image": "images/vegetables/tomato.jpg",
      "is_correct": false,
      "confidence": 0.9,
      "explanation": "Shows a fruit icon instead of actual tomato"
    }
  ],
  "all_results": [...]
}
```

## Examples

### Check all vegetables:
```powershell
python verify_images_with_ai.py
# Choose option 2
# Enter: Vegetables
```

### Check all landmarks:
```powershell
python verify_images_with_ai.py
# Choose option 2
# Enter: Landmarks
```

### Check everything (warning: will use significant API credits):
```powershell
python verify_images_with_ai.py
# Choose option 1
# Confirm with: yes
```

## Cost & Performance

### Cost
**$0.00 - Completely FREE!**
- No API keys required
- No cloud services
- Runs entirely on your computer
- Models downloaded once, cached forever

### Performance
- **First run**: 2-5 minutes (downloads models ~500MB)
- **Subsequent runs**: Fast (models are cached)
- **Speed**: ~2-5 seconds per image (depends on your computer)
- **Accuracy**: Good for most common objects, may struggle with very specific items

### System Requirements
- **Storage**: ~1GB for AI models (one-time download)
- **RAM**: 4GB+ recommended
- **GPU**: Optional - runs on CPU, faster with NVIDIA GPU

## Tips

1. **Start small**: Test with a single category first
2. **Review confidence scores**: Low confidence (<0.7) may need manual review
3. **Check the report**: Review `image_verification_report.json` for detailed analysis
4. **False positives**: The AI is conservative - some correct images may be flagged if unclear

## Troubleshooting

### "No module named 'transformers'"
Install required libraries:
```powershell
pip install transformers torch torchvision pillow
```

### "Models downloading slowly"
First-time model download is ~500MB. Be patient - it only happens once!

### "Out of memory" error
The models use RAM. Close other applications or:
- Check one category at a time instead of all images
- Restart your computer to free up memory

### Low accuracy / many false positives
The free AI models are good but not perfect. They work best for:
- ✅ Common objects (fruits, animals, vehicles)
- ✅ Clear, well-lit photos
- ❌ Abstract concepts or very specific items
- ❌ Icons/logos (it expects real photos)

For critical verification, manually review flagged images.

## What the AI Checks

The AI evaluates:
- ✅ Does the image clearly show the expected item?
- ✅ Is it a photo/realistic image (not just a logo or icon)?
- ✅ Is the item the main subject of the image?
- ❌ Flags images that are unclear, low quality, or show wrong items
- ❌ Flags generic icons/logos instead of actual items

## Next Steps

After verification:
1. Review the `incorrect_images` list in the JSON report
2. Manually verify flagged images
3. Re-download incorrect images using the existing download scripts
4. Re-run verification to confirm fixes
