#!/usr/bin/env python3
"""
Demo script for Car Damage Detection System
This script demonstrates how to use the damage detection system programmatically.
"""

import os
from simple_damage_detector import detect_damage, display_result

def demo_single_image():
    """Demo with a single image."""
    print("=== Demo: Single Image Detection ===")
    
    # Example image path (you can change this to your own image)
    image_path = "data1a/training/00-damage/0001.JPEG"
    
    if os.path.exists(image_path):
        print(f"Testing image: {image_path}")
        
        # Detect damage
        result = detect_damage(image_path)
        
        if result:
            status = "DAMAGED" if result['is_damaged'] else "NOT DAMAGED"
            print(f"Result: {status}")
            print(f"Confidence: {result['confidence_percent']:.2f}%")
            print(f"Class: {result['class_label']}")
            
            # Display the image with results
            display_result(image_path, result)
        else:
            print("Failed to process image")
    else:
        print(f"Image not found: {image_path}")

def demo_multiple_images():
    """Demo with multiple images."""
    print("\n=== Demo: Multiple Images Detection ===")
    
    # List of test images
    test_images = [
        ("data1a/training/00-damage/0001.JPEG", "Damaged car"),
        ("data1a/training/01-whole/0001.jpg", "Undamaged car"),
        ("data1a/validation/00-damage/0001.JPEG", "Damaged car (validation)"),
        ("data1a/validation/01-whole/0001.jpg", "Undamaged car (validation)")
    ]
    
    results_summary = []
    
    for image_path, description in test_images:
        if os.path.exists(image_path):
            print(f"\nTesting: {description}")
            print(f"Image: {image_path}")
            
            result = detect_damage(image_path)
            
            if result:
                status = "DAMAGED" if result['is_damaged'] else "NOT DAMAGED"
                confidence = result['confidence_percent']
                
                print(f"Result: {status} (Confidence: {confidence:.2f}%)")
                
                results_summary.append({
                    'description': description,
                    'status': status,
                    'confidence': confidence,
                    'expected': 'DAMAGED' if 'damage' in image_path else 'NOT DAMAGED'
                })
            else:
                print("Failed to process image")
        else:
            print(f"Image not found: {image_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY OF RESULTS:")
    print("="*60)
    
    correct_predictions = 0
    total_predictions = len(results_summary)
    
    for result in results_summary:
        is_correct = result['status'] == result['expected']
        if is_correct:
            correct_predictions += 1
        
        status_icon = "✓" if is_correct else "✗"
        print(f"{status_icon} {result['description']:30} | "
              f"Expected: {result['expected']:12} | "
              f"Predicted: {result['status']:12} | "
              f"Confidence: {result['confidence']:6.2f}%")
    
    accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
    print(f"\nOverall Accuracy: {accuracy:.1f}% ({correct_predictions}/{total_predictions})")

def demo_custom_image():
    """Demo with a custom image path."""
    print("\n=== Demo: Custom Image Detection ===")
    
    # You can change this path to test your own images
    custom_image_path = input("Enter the path to your car image (or press Enter to skip): ").strip()
    
    if custom_image_path and os.path.exists(custom_image_path):
        print(f"Testing your image: {custom_image_path}")
        
        result = detect_damage(custom_image_path)
        
        if result:
            status = "DAMAGED" if result['is_damaged'] else "NOT DAMAGED"
            print(f"Result: {status}")
            print(f"Confidence: {result['confidence_percent']:.2f}%")
            print(f"Class: {result['class_label']}")
            
            # Ask if user wants to display the image
            show_image = input("Do you want to display the image with results? (y/n): ").strip().lower()
            if show_image in ['y', 'yes']:
                display_result(custom_image_path, result)
        else:
            print("Failed to process your image")
    elif custom_image_path:
        print(f"Image not found: {custom_image_path}")
    else:
        print("Skipping custom image demo")

def main():
    """Main demo function."""
    print("🚗 Car Damage Detection System - Demo")
    print("=" * 50)
    
    # Check if model exists
    if not os.path.exists("damage_detection.h5"):
        print("❌ Error: Model file 'damage_detection.h5' not found!")
        print("Please make sure the trained model is in the current directory.")
        return
    
    print("✅ Model file found!")
    print()
    
    # Run demos
    try:
        demo_single_image()
        demo_multiple_images()
        demo_custom_image()
        
        print("\n" + "="*50)
        print("🎉 Demo completed successfully!")
        print("\nTo use the system:")
        print("1. Run 'python simple_damage_detector.py' for interactive mode")
        print("2. Run 'python damage_detector.py' for GUI mode")
        print("3. Import the functions in your own code")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")

if __name__ == "__main__":
    main() 