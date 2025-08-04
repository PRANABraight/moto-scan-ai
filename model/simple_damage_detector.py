import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import matplotlib.pyplot as plt

def detect_damage(image_path, model_path="damage_detection.h5"):
    """
    Detect if a car image shows damage or not.
    
    Args:
        image_path (str): Path to the image file
        model_path (str): Path to the trained model file
    
    Returns:
        dict: Prediction results with status, confidence, and class
    """
    
    # Check if files exist
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return None
    
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found.")
        return None
    
    try:
        # Load the trained model
        print("Loading model...")
        model = load_model(model_path)
        
        # Load and preprocess the image
        print("Processing image...")
        image = load_img(image_path, target_size=(224, 224))
        image_array = img_to_array(image)
        image_array = np.expand_dims(image_array, axis=0)
        image_array = preprocess_input(image_array)
        
        # Make prediction
        print("Making prediction...")
        prediction = model.predict(image_array)
        predicted_class = np.argmax(prediction[0])
        confidence = prediction[0][predicted_class]
        
        # Class labels
        classes = ["00-damage", "01-whole"]
        class_label = classes[predicted_class]
        is_damaged = class_label == "00-damage"
        
        result = {
            'is_damaged': is_damaged,
            'class_label': class_label,
            'confidence': confidence,
            'confidence_percent': confidence * 100
        }
        
        return result
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

def display_result(image_path, result):
    """Display the image and prediction result."""
    if result is None:
        return
    
    # Load and display image
    image = plt.imread(image_path)
    
    plt.figure(figsize=(12, 6))
    
    # Display image
    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title("Input Image")
    plt.axis('off')
    
    # Display result
    plt.subplot(1, 2, 2)
    status = "DAMAGED" if result['is_damaged'] else "NOT DAMAGED"
    color = 'red' if result['is_damaged'] else 'green'
    
    plt.text(0.5, 0.6, f"Status: {status}", 
             fontsize=20, fontweight='bold', color=color, 
             ha='center', va='center', transform=plt.gca().transAxes)
    
    plt.text(0.5, 0.4, f"Confidence: {result['confidence_percent']:.2f}%", 
             fontsize=16, ha='center', va='center', transform=plt.gca().transAxes)
    
    plt.text(0.5, 0.2, f"Class: {result['class_label']}", 
             fontsize=14, ha='center', va='center', transform=plt.gca().transAxes)
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def main():
    """Main function to run the damage detector."""
    print("=== Car Damage Detection System ===")
    print("This system can detect if a car image shows damage or not.")
    print()
    
    # Get image path from user
    while True:
        image_path = input("Enter the path to your car image: ").strip()
        
        if not image_path:
            print("Please enter a valid image path.")
            continue
            
        if image_path.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        # Detect damage
        result = detect_damage(image_path)
        
        if result:
            print("\n" + "="*50)
            status = "DAMAGED" if result['is_damaged'] else "NOT DAMAGED"
            print(f"RESULT: {status}")
            print(f"Confidence: {result['confidence_percent']:.2f}%")
            print(f"Class: {result['class_label']}")
            print("="*50)
            
            # Ask if user wants to display the image
            show_image = input("\nDo you want to display the image with results? (y/n): ").strip().lower()
            if show_image in ['y', 'yes']:
                display_result(image_path, result)
        
        print("\n" + "-"*50)

if __name__ == "__main__":
    main() 