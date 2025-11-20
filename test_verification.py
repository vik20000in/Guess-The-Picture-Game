"""
Quick test script to verify the AI image verification is working.
Tests on a few sample images before running on the entire dataset.
"""

from verify_images_with_ai import verify_specific_images
import os

def test_verification():
    """Test the verification on a few sample images."""
    
    print("="*60)
    print("TESTING AI IMAGE VERIFICATION")
    print("="*60)
    print()
    print("This will test the AI on a few sample images...")
    print("Models will be downloaded on first run (~500MB)")
    print()
    
    # Find some test images
    test_specs = []
    
    # Try to find a few images to test
    test_categories = [
        ('images/fruits/apple.jpg', 'Apple', 'Fruits'),
        ('images/vegetables/tomato.jpg', 'Tomato', 'Vegetables'),
        ('images/animals/dog.jpg', 'Dog', 'Animals'),
        ('images/birds/peacock.jpg', 'Peacock', 'Birds'),
        ('images/landmarks/eiffel_tower.jpg', 'Eiffel Tower', 'Landmarks'),
    ]
    
    for img_path, item_name, category in test_categories:
        if os.path.exists(img_path):
            test_specs.append((img_path, item_name, category))
            if len(test_specs) >= 3:  # Test with 3 images
                break
    
    if not test_specs:
        print("❌ No test images found. Please make sure some category images exist.")
        return
    
    print(f"Testing with {len(test_specs)} sample images:")
    for img_path, item_name, category in test_specs:
        print(f"  - {item_name} ({category})")
    print()
    
    # Run verification
    results = verify_specific_images(test_specs)
    
    # Summary
    print()
    print("="*60)
    print("TEST COMPLETE!")
    print("="*60)
    
    if results:
        correct = sum(1 for r in results if r['is_correct'])
        print(f"✅ Verified {len(results)} images")
        print(f"✅ {correct}/{len(results)} marked as correct")
        print()
        print("The AI verification system is working!")
        print("You can now run the full verification with:")
        print("  python verify_images_with_ai.py")
    else:
        print("⚠️ No results returned. Check for errors above.")

if __name__ == "__main__":
    test_verification()
