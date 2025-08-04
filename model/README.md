# Car Damage Detection System

This system uses a trained deep learning model to detect whether a car image shows damage or not. The model is based on MobileNetV2 and has been trained on a dataset of car images.

## Features

- **Simple Command Line Interface**: Easy-to-use script for quick damage detection
- **GUI Interface**: Full graphical interface with file selection and webcam support
- **Real-time Webcam Detection**: Live damage detection using your webcam
- **High Accuracy**: Trained model with ~88% accuracy on validation data

## Files

- `simple_damage_detector.py` - Simple command-line interface (recommended for beginners)
- `damage_detector.py` - Full GUI interface with webcam support
- `test_detector.py` - Test script to verify the system works
- `damage_detection.h5` - Trained model file
- `Specialisation.ipynb` - Original training notebook

## Quick Start

### Method 1: Simple Command Line Interface (Recommended)

1. **Run the simple detector:**
   ```bash
   python simple_damage_detector.py
   ```

2. **Enter the path to your car image when prompted:**
   ```
   Enter the path to your car image: path/to/your/car/image.jpg
   ```

3. **View the results:**
   - The system will tell you if the car is DAMAGED or NOT DAMAGED
   - It will show the confidence level of the prediction
   - You can choose to display the image with results

### Method 2: GUI Interface

1. **Run the GUI version:**
   ```bash
   python damage_detector.py
   ```

2. **Choose interface:**
   - Select option 1 for GUI interface

3. **Use the interface:**
   - Click "Select Image File" to browse for an image
   - Click "Use Webcam" for real-time detection
   - Drag and drop images into the designated area

### Method 3: Test the System

1. **Run the test script:**
   ```bash
   python test_detector.py
   ```

2. **This will test the system with sample images from your dataset**

## How to Use

### Input Image Requirements

- **Supported formats**: JPG, JPEG, PNG, BMP, GIF, TIFF
- **Image content**: Should contain a car (preferably centered)
- **Image quality**: Higher resolution images work better
- **Lighting**: Well-lit images give better results

### Understanding Results

- **DAMAGED**: The model detected damage in the car image
- **NOT DAMAGED**: The model detected no damage in the car image
- **Confidence**: Percentage indicating how certain the model is (higher is better)
- **Class**: Technical class label (00-damage or 01-whole)

### Example Usage

```python
from simple_damage_detector import detect_damage

# Detect damage in an image
result = detect_damage("path/to/car_image.jpg")

if result:
    status = "DAMAGED" if result['is_damaged'] else "NOT DAMAGED"
    print(f"Car is: {status}")
    print(f"Confidence: {result['confidence_percent']:.2f}%")
```

## Model Information

- **Architecture**: MobileNetV2 with custom head
- **Input size**: 224x224 pixels
- **Classes**: 2 (damaged, not damaged)
- **Training data**: 1,840 training images, 460 validation images
- **Accuracy**: ~88% on validation set

## Troubleshooting

### Common Issues

1. **"Model file not found"**
   - Make sure `damage_detection.h5` is in the same directory
   - Check if the file was downloaded correctly

2. **"Image file not found"**
   - Verify the image path is correct
   - Use absolute paths if needed

3. **"Failed to process image"**
   - Try a different image format
   - Ensure the image contains a car
   - Check if the image is corrupted

4. **Webcam not working**
   - Ensure your webcam is connected and working
   - Check if another application is using the webcam
   - Try restarting the application

### Performance Tips

- **Use high-quality images** for better accuracy
- **Ensure good lighting** in the image
- **Center the car** in the image when possible
- **Avoid extreme angles** that might confuse the model

## Technical Details

### Model Architecture

The model uses a pre-trained MobileNetV2 as the base with a custom classification head:

1. **Base Model**: MobileNetV2 (pre-trained on ImageNet)
2. **Global Max Pooling**: 5x5 pool size
3. **Flatten Layer**: Converts features to 1D
4. **Dense Layer**: 128 units with ReLU activation
5. **Dropout**: 50% dropout for regularization
6. **Output Layer**: 2 units with softmax activation

### Training Details

- **Optimizer**: Adam with learning rate 0.001
- **Loss Function**: Binary cross-entropy
- **Data Augmentation**: Rotation, zoom, shift, shear, horizontal flip
- **Batch Size**: 64
- **Epochs**: 100

## Requirements

Make sure you have the following Python packages installed:

```bash
pip install tensorflow opencv-python matplotlib numpy pillow
```

Or install from the requirements file:

```bash
pip install -r requirements.txt
```

## Dataset

The model was trained on a car damage detection dataset with:
- **Training**: 920 damaged + 920 not damaged images
- **Validation**: 230 damaged + 230 not damaged images
- **Total**: 2,300 images

## License

This project is for educational purposes. The model and code are provided as-is.

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all files are in the correct locations
3. Ensure all dependencies are installed
4. Try the test script to verify the system works 