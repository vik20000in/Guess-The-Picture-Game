"""
Image Verification Script using AI (Free - No API Key Required)
This script uses local AI models (BLIP-2) to verify if images match their expected content.
Runs completely offline after initial model download.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Tuple
import time
from difflib import SequenceMatcher

# Try to import required libraries
try:
    from PIL import Image
    from transformers import BlipProcessor, BlipForConditionalGeneration, BlipForQuestionAnswering
    import torch
except ImportError:
    print("Required libraries not installed. Installing...")
    print("This may take a few minutes...")
    import subprocess
    subprocess.check_call(["pip", "install", "transformers", "torch", "torchvision", "pillow"])
    from PIL import Image
    from transformers import BlipProcessor, BlipForConditionalGeneration, BlipForQuestionAnswering
    import torch


class LocalImageVerifier:
    """Local AI-based image verifier using BLIP model (free, no API key needed)."""
    
    def __init__(self):
        """Initialize the BLIP model for image captioning and VQA."""
        print("Loading AI models (this may take a minute on first run)...")
        print("Models will be cached for future use...")
        
        # Use BLIP for image captioning
        self.caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        
        # Use BLIP for visual question answering
        self.vqa_processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
        self.vqa_model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
        
        # Determine device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.caption_model.to(self.device)
        self.vqa_model.to(self.device)
        
        print(f"✅ Models loaded successfully! (Using {self.device.upper()})")
        print()
    
    def get_image_caption(self, image_path: str) -> str:
        """Generate a caption for the image."""
        try:
            image = Image.open(image_path).convert('RGB')
            inputs = self.caption_processor(image, return_tensors="pt").to(self.device)
            out = self.caption_model.generate(**inputs, max_length=50)
            caption = self.caption_processor.decode(out[0], skip_special_tokens=True)
            return caption
        except Exception as e:
            return f"Error: {str(e)}"
    
    def ask_question(self, image_path: str, question: str) -> str:
        """Ask a question about the image."""
        try:
            image = Image.open(image_path).convert('RGB')
            inputs = self.vqa_processor(image, question, return_tensors="pt").to(self.device)
            out = self.vqa_model.generate(**inputs, max_length=20)
            answer = self.vqa_processor.decode(out[0], skip_special_tokens=True)
            return answer
        except Exception as e:
            return f"Error: {str(e)}"
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two strings."""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def verify_image(self, image_path: str, expected_item: str, category: str) -> Tuple[bool, str, float]:
        """
        Verify if an image matches the expected item.
        
        Returns:
            Tuple of (is_correct, explanation, confidence_score)
        """
        try:
            # Get image caption
            caption = self.get_image_caption(image_path)
            
            # Ask specific questions
            q1 = f"What is this?"
            a1 = self.ask_question(image_path, q1)
            
            q2 = f"Is this a {expected_item}?"
            a2 = self.ask_question(image_path, q2)
            
            # Calculate similarities
            caption_similarity = self.calculate_similarity(caption, expected_item)
            answer_similarity = self.calculate_similarity(a1, expected_item)
            
            # Check if direct question got positive answer
            yes_no_answer = a2.lower()
            is_yes = any(word in yes_no_answer for word in ['yes', 'yeah', 'correct', 'true'])
            is_no = any(word in yes_no_answer for word in ['no', 'not', 'incorrect', 'false'])
            
            # Scoring logic
            score = 0.0
            
            # Check if expected item name appears in caption or answer
            if expected_item.lower() in caption.lower():
                score += 0.4
            if expected_item.lower() in a1.lower():
                score += 0.3
            
            # Similarity scores
            score += caption_similarity * 0.2
            score += answer_similarity * 0.2
            
            # Yes/No question bonus
            if is_yes:
                score += 0.3
            elif is_no:
                score -= 0.3
            
            # Determine if correct (threshold: 0.5)
            is_correct = score >= 0.5
            confidence = min(max(score, 0.0), 1.0)
            
            # Build explanation
            explanation = f"Caption: '{caption}'. "
            if a1 and "error" not in a1.lower():
                explanation += f"AI identifies this as: '{a1}'. "
            if a2 and "error" not in a2.lower():
                explanation += f"Is it a {expected_item}? {a2}."
            
            return is_correct, explanation, confidence
            
        except Exception as e:
            return False, f"Error: {str(e)}", 0.0


# Global verifier instance
_verifier = None


def get_verifier():
    """Get or create the global verifier instance."""
    global _verifier
    if _verifier is None:
        _verifier = LocalImageVerifier()
    return _verifier


def verify_image_with_ai(verifier, image_path: str, expected_item: str, category: str) -> Tuple[bool, str, float]:
    """
    Verify if an image matches the expected item using local AI.
    
    Returns:
        Tuple of (is_correct, explanation, confidence_score)
    """
    return verifier.verify_image(image_path, expected_item, category)


def load_category_data(category_file: str) -> List[Dict]:
    """Load category data from JSON file."""
    with open(category_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def verify_all_images(api_key: str = None, categories_to_check: List[str] = None):
    """
    Verify all images in the game against their expected content.
    
    Args:
        api_key: Not used (kept for compatibility)
        categories_to_check: List of category names to check (if None, checks all)
    """
    # Initialize local AI verifier (no API key needed!)
    verifier = get_verifier()
    
    # Load categories
    with open('categories.json', 'r', encoding='utf-8') as f:
        categories = json.load(f)
    
    # Results tracking
    all_results = []
    incorrect_images = []
    total_checked = 0
    total_incorrect = 0
    
    # Check each category
    for category in categories:
        category_name = category['name']
        
        # Skip if we're filtering categories
        if categories_to_check and category_name not in categories_to_check:
            continue
        
        data_file = category.get('dataFile')
        if not data_file or not os.path.exists(data_file):
            print(f"Skipping {category_name} - no data file found")
            continue
        
        print(f"\n{'='*60}")
        print(f"Checking category: {category_name}")
        print(f"{'='*60}")
        
        # Load items
        items = load_category_data(data_file)
        
        # Check each item
        for item in items:
            item_name = item.get('name', 'Unknown')
            image_path = item.get('image', '')
            
            if not image_path or not os.path.exists(image_path):
                print(f"⚠️  {item_name}: Image file not found - {image_path}")
                incorrect_images.append({
                    'category': category_name,
                    'item': item_name,
                    'image': image_path,
                    'issue': 'File not found',
                    'confidence': 0.0
                })
                continue
            
            # Verify image
            print(f"Checking: {item_name}...", end=' ')
            is_correct, explanation, confidence = verify_image_with_ai(
                verifier, image_path, item_name, category_name
            )
            
            total_checked += 1
            
            result = {
                'category': category_name,
                'item': item_name,
                'image': image_path,
                'is_correct': is_correct,
                'confidence': confidence,
                'explanation': explanation
            }
            all_results.append(result)
            
            if is_correct:
                print(f"✅ CORRECT (confidence: {confidence:.2f})")
            else:
                print(f"❌ INCORRECT (confidence: {confidence:.2f})")
                print(f"   Reason: {explanation}")
                total_incorrect += 1
                incorrect_images.append(result)
            
            # Rate limiting - small delay between requests (for system stability)
            time.sleep(0.2)
    
    # Generate report
    print(f"\n{'='*60}")
    print(f"VERIFICATION COMPLETE")
    print(f"{'='*60}")
    print(f"Total images checked: {total_checked}")
    print(f"Correct images: {total_checked - total_incorrect}")
    print(f"Incorrect/Suspicious images: {total_incorrect}")
    print(f"Accuracy: {((total_checked - total_incorrect) / total_checked * 100) if total_checked > 0 else 0:.1f}%")
    
    # Save detailed report
    report_file = 'image_verification_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'total_checked': total_checked,
                'correct': total_checked - total_incorrect,
                'incorrect': total_incorrect,
                'accuracy_percent': ((total_checked - total_incorrect) / total_checked * 100) if total_checked > 0 else 0
            },
            'incorrect_images': incorrect_images,
            'all_results': all_results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed report saved to: {report_file}")
    
    # Print incorrect images summary
    if incorrect_images:
        print(f"\n{'='*60}")
        print(f"INCORRECT/SUSPICIOUS IMAGES:")
        print(f"{'='*60}")
        for img in incorrect_images:
            print(f"\n📁 {img['category']} - {img['item']}")
            print(f"   File: {img['image']}")
            print(f"   Issue: {img.get('explanation', img.get('issue', 'Unknown'))}")
            print(f"   Confidence: {img.get('confidence', 0):.2f}")
    
    return all_results, incorrect_images


def verify_single_category(category_name: str, api_key: str = None):
    """Verify images for a single category."""
    return verify_all_images(api_key=api_key, categories_to_check=[category_name])


def verify_specific_images(image_specs: List[Tuple[str, str, str]], api_key: str = None):
    """
    Verify specific images.
    
    Args:
        image_specs: List of tuples (image_path, expected_item, category)
        api_key: Not used (kept for compatibility)
    """
    verifier = get_verifier()
    
    results = []
    for image_path, expected_item, category in image_specs:
        print(f"Checking {expected_item} ({category})...", end=' ')
        is_correct, explanation, confidence = verify_image_with_ai(
            verifier, image_path, expected_item, category
        )
        
        result = {
            'image': image_path,
            'item': expected_item,
            'category': category,
            'is_correct': is_correct,
            'confidence': confidence,
            'explanation': explanation
        }
        results.append(result)
        
        status = "✅ CORRECT" if is_correct else "❌ INCORRECT"
        print(f"{status} (confidence: {confidence:.2f})")
        if not is_correct:
            print(f"   Reason: {explanation}")
    
    return results


if __name__ == "__main__":
    import sys
    
    print("="*60)
    print("IMAGE VERIFICATION TOOL - FREE LOCAL AI")
    print("No API Key Required - Runs on Your Computer")
    print("="*60)
    print()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        # Command line mode: python verify_images_with_ai.py CategoryName
        category_name = " ".join(sys.argv[1:])
        print(f"Verifying category: {category_name}")
        print()
        verify_single_category(category_name)
    else:
        # Interactive menu mode
        print("\nWhat would you like to do?")
        print("1. Verify all images in all categories")
        print("2. Verify a specific category")
        print("3. Verify multiple categories")
        print("4. Verify specific images")
        print()
        print("💡 Tip: You can also run: python verify_images_with_ai.py CategoryName")
        print()
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            print("\nStarting verification of ALL images...")
            print("⚠️  WARNING: This will check 500+ images and may take 30+ minutes!")
            confirm = input("Continue? (yes/no): ").strip().lower()
            if confirm == 'yes':
                verify_all_images()
            else:
                print("Cancelled.")
        
        elif choice == "2":
            print("\nAvailable categories:")
            with open('categories.json', 'r', encoding='utf-8') as f:
                categories = json.load(f)
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat['name']}")
            
            cat_choice = input("\nEnter category name or number: ").strip()
            
            # Handle numeric input
            if cat_choice.isdigit():
                idx = int(cat_choice) - 1
                if 0 <= idx < len(categories):
                    cat_choice = categories[idx]['name']
                else:
                    print("Invalid category number.")
                    sys.exit(1)
            
            verify_single_category(cat_choice)
        
        elif choice == "3":
            print("\nAvailable categories:")
            with open('categories.json', 'r', encoding='utf-8') as f:
                categories = json.load(f)
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat['name']}")
            
            print("\nEnter category names or numbers (comma-separated)")
            print("Example: 1,3,5 or Vegetables,Birds,Flowers")
            cat_input = input("> ").strip()
            
            if not cat_input:
                print("No categories specified.")
            else:
                selected_cats = []
                parts = [p.strip() for p in cat_input.split(',')]
                
                for part in parts:
                    if part.isdigit():
                        idx = int(part) - 1
                        if 0 <= idx < len(categories):
                            selected_cats.append(categories[idx]['name'])
                    else:
                        # Try to find matching category name
                        matches = [c['name'] for c in categories if c['name'].lower() == part.lower()]
                        if matches:
                            selected_cats.append(matches[0])
                        else:
                            print(f"⚠️  Category '{part}' not found, skipping...")
                
                if selected_cats:
                    print(f"\nVerifying {len(selected_cats)} categories: {', '.join(selected_cats)}")
                    verify_all_images(categories_to_check=selected_cats)
                else:
                    print("No valid categories selected.")
        
        elif choice == "4":
            print("\nEnter image details (format: image_path,expected_item,category)")
            print("Example: images/fruits/apple.jpg,Apple,Fruits")
            print("Enter blank line when done.")
            
            image_specs = []
            while True:
                line = input("> ").strip()
                if not line:
                    break
                parts = [p.strip() for p in line.split(',')]
                if len(parts) == 3:
                    image_specs.append(tuple(parts))
                else:
                    print("Invalid format. Use: image_path,expected_item,category")
            
            if image_specs:
                verify_specific_images(image_specs)
            else:
                print("No images specified.")
        
        else:
            print("Invalid choice.")
