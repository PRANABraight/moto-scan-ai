import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading

class DamageDetector:
    def __init__(self, model_path="damage_detection.h5"):
        """Initialize the damage detector with the trained model."""
        self.model = load_model(model_path)
        self.classes = ["00-damage", "01-whole"]
        self.target_size = (224, 224)
        
    def preprocess_image(self, image_path):
        """Preprocess a single image for prediction."""
        # Load and resize image
        image = load_img(image_path, target_size=self.target_size)
        # Convert to array
        image_array = img_to_array(image)
        # Expand dimensions for batch prediction
        image_array = np.expand_dims(image_array, axis=0)
        # Preprocess for MobileNetV2
        image_array = preprocess_input(image_array)
        return image_array
    
    def predict_damage(self, image_path):
        """Predict whether an image shows damage or not."""
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image_path)
            
            # Make prediction
            prediction = self.model.predict(processed_image)
            predicted_class = np.argmax(prediction[0])
            confidence = prediction[0][predicted_class]
            
            # Get class label
            class_label = self.classes[predicted_class]
            is_damaged = class_label == "00-damage"
            
            return {
                'is_damaged': is_damaged,
                'class_label': class_label,
                'confidence': confidence,
                'prediction': prediction[0]
            }
            
        except Exception as e:
            print(f"Error predicting image: {e}")
            return None
    
    def predict_from_array(self, image_array):
        """Predict from a numpy array (for webcam)."""
        try:
            # Resize image
            image_resized = cv2.resize(image_array, self.target_size)
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
            # Convert to array and preprocess
            image_array = img_to_array(image_rgb)
            image_array = np.expand_dims(image_array, axis=0)
            image_array = preprocess_input(image_array)
            
            # Make prediction
            prediction = self.model.predict(image_array)
            predicted_class = np.argmax(prediction[0])
            confidence = prediction[0][predicted_class]
            
            class_label = self.classes[predicted_class]
            is_damaged = class_label == "00-damage"
            
            return {
                'is_damaged': is_damaged,
                'class_label': class_label,
                'confidence': confidence,
                'prediction': prediction[0]
            }
            
        except Exception as e:
            print(f"Error predicting from array: {e}")
            return None

class DamageDetectorGUI:
    def __init__(self):
        """Initialize the GUI for damage detection."""
        self.detector = DamageDetector()
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the graphical user interface."""
        self.root = tk.Tk()
        self.root.title("Car Damage Detector")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Title
        title_label = tk.Label(self.root, text="Car Damage Detection System", 
                              font=("Arial", 20, "bold"), bg='#f0f0f0')
        title_label.pack(pady=20)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        # File selection button
        self.file_button = tk.Button(button_frame, text="Select Image File", 
                                    command=self.select_file, 
                                    font=("Arial", 12), bg='#4CAF50', fg='white',
                                    width=15, height=2)
        self.file_button.pack(side=tk.LEFT, padx=10)
        
        # Webcam button
        self.webcam_button = tk.Button(button_frame, text="Use Webcam", 
                                      command=self.start_webcam, 
                                      font=("Arial", 12), bg='#2196F3', fg='white',
                                      width=15, height=2)
        self.webcam_button.pack(side=tk.LEFT, padx=10)
        
        # Drag and drop area
        self.drop_frame = tk.Frame(self.root, bg='#e0e0e0', relief=tk.RAISED, bd=2)
        self.drop_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        self.drop_label = tk.Label(self.drop_frame, text="Drag and drop image here\nor click to browse", 
                                  font=("Arial", 14), bg='#e0e0e0')
        self.drop_label.pack(expand=True)
        
        # Bind click event to drop area
        self.drop_frame.bind("<Button-1>", lambda e: self.select_file())
        
        # Results area
        self.result_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.result_frame.pack(pady=20, fill=tk.X, padx=50)
        
        self.result_label = tk.Label(self.result_frame, text="", 
                                    font=("Arial", 12), bg='#f0f0f0', wraplength=700)
        self.result_label.pack()
        
        # Image display area
        self.image_label = tk.Label(self.root, bg='#f0f0f0')
        self.image_label.pack(pady=10)
        
        # Webcam variables
        self.webcam_active = False
        self.cap = None
        
    def select_file(self):
        """Open file dialog to select an image."""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        
        if file_path:
            self.process_image(file_path)
    
    def process_image(self, image_path):
        """Process the selected image and display results."""
        # Make prediction
        result = self.detector.predict_damage(image_path)
        
        if result:
            # Display image
            self.display_image(image_path)
            
            # Display results
            status = "DAMAGED" if result['is_damaged'] else "NOT DAMAGED"
            color = "red" if result['is_damaged'] else "green"
            confidence_percent = result['confidence'] * 100
            
            result_text = f"Status: {status}\nConfidence: {confidence_percent:.2f}%"
            self.result_label.config(text=result_text, fg=color, font=("Arial", 14, "bold"))
        else:
            messagebox.showerror("Error", "Failed to process the image. Please try again.")
    
    def display_image(self, image_path):
        """Display the selected image in the GUI."""
        try:
            # Load and resize image for display
            image = Image.open(image_path)
            # Resize while maintaining aspect ratio
            display_size = (400, 300)
            image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Update label
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference
            
        except Exception as e:
            print(f"Error displaying image: {e}")
    
    def start_webcam(self):
        """Start webcam for real-time damage detection."""
        if not self.webcam_active:
            self.webcam_active = True
            self.webcam_button.config(text="Stop Webcam", bg='#f44336')
            
            # Start webcam in a separate thread
            webcam_thread = threading.Thread(target=self.webcam_loop)
            webcam_thread.daemon = True
            webcam_thread.start()
        else:
            self.stop_webcam()
    
    def stop_webcam(self):
        """Stop the webcam."""
        self.webcam_active = False
        self.webcam_button.config(text="Use Webcam", bg='#2196F3')
        if self.cap:
            self.cap.release()
    
    def webcam_loop(self):
        """Main webcam loop for real-time detection."""
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam")
            self.stop_webcam()
            return
        
        while self.webcam_active:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Make prediction
            result = self.detector.predict_from_array(frame)
            
            if result:
                # Draw results on frame
                status = "DAMAGED" if result['is_damaged'] else "NOT DAMAGED"
                color = (0, 0, 255) if result['is_damaged'] else (0, 255, 0)
                confidence = result['confidence'] * 100
                
                cv2.putText(frame, f"{status}: {confidence:.1f}%", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            # Display frame
            cv2.imshow("Car Damage Detection - Webcam", frame)
            
            # Break on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
        self.stop_webcam()
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

def simple_command_line_detector():
    """Simple command-line interface for damage detection."""
    detector = DamageDetector()
    
    print("=== Car Damage Detection System ===")
    print("Enter the path to an image file (or 'quit' to exit):")
    
    while True:
        image_path = input("\nImage path: ").strip()
        
        if image_path.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not os.path.exists(image_path):
            print("Error: File not found. Please enter a valid path.")
            continue
        
        # Make prediction
        result = detector.predict_damage(image_path)
        
        if result:
            status = "DAMAGED" if result['is_damaged'] else "NOT DAMAGED"
            confidence = result['confidence'] * 100
            
            print(f"\nResult: {status}")
            print(f"Confidence: {confidence:.2f}%")
            print(f"Class: {result['class_label']}")
        else:
            print("Error: Failed to process the image.")

if __name__ == "__main__":
    print("Car Damage Detection System")
    print("1. GUI Interface (recommended)")
    print("2. Command Line Interface")
    
    choice = input("Choose interface (1 or 2): ").strip()
    
    if choice == "1":
        # Start GUI
        app = DamageDetectorGUI()
        app.run()
    elif choice == "2":
        # Start command line interface
        simple_command_line_detector()
    else:
        print("Invalid choice. Starting GUI by default...")
        app = DamageDetectorGUI()
        app.run() 