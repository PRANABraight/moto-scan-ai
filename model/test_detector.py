import os
from simple_damage_detector import detect_damage

def test_damage_detector():
    """Test the damage detector with sample images from the dataset."""
    
    print("=== Testing Car Damage Detection System ===")
    
    # Test with sample images from the dataset
    test_images = [
        "data1a/training/00-damage/0001.JPEG",  # Should be detected as damaged
        "data1a/training/01-whole/0001.jpg",    # Should be detected as not damaged
    ]
    
    for image_path in test_images:
        if os.path.exists(image_path):
            print(f"\nTesting image: {image_path}")
            print("-" * 40)
            
            result = detect_damage(image_path)
            
            if result:
                status = "DAMAGED" if result['is_damaged'] else "NOT DAMAGED"
                print(f"Expected: {'DAMAGED' if 'damage' in image_path else 'NOT DAMAGED'}")
                print(f"Predicted: {status}")
                print(f"Confidence: {result['confidence_percent']:.2f}%")
                print(f"Class: {result['class_label']}")
                
                # Check if prediction matches expected
                expected_damaged = 'damage' in image_path
                if result['is_damaged'] == expected_damaged:
                    print("✓ Prediction is CORRECT!")
                else:
                    print("✗ Prediction is INCORRECT!")
            else:
                print("Failed to process image")
        else:
            print(f"Test image not found: {image_path}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_damage_detector() 