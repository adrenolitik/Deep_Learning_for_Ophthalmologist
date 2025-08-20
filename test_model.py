#!/usr/bin/env python3
"""
Test script to verify the diabetic retinopathy detection model can be loaded correctly.
Run this before starting the main app to check for any issues.
"""

import torch
import torch.nn as nn
from torchvision import models
import os

def test_model_loading():
    """Test if the model can be loaded successfully."""
    print("🔍 Testing model loading...")
    
    try:
        # Check if model file exists
        model_path = "resnet50_dr_classifier.pth"
        if not os.path.exists(model_path):
            print(f"❌ Error: Model file '{model_path}' not found!")
            print("   Please ensure the model file is in the current directory.")
            return False
        
        print(f"✅ Model file found: {model_path}")
        
        # Check file size
        file_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
        print(f"📁 Model file size: {file_size:.2f} MB")
        
        # Try to load the model
        device = torch.device("cpu")
        print("🔄 Loading model...")
        
        model = models.resnet50(weights=None)
        model.fc = nn.Linear(model.fc.in_features, 2)
        
        # Load state dict
        state_dict = torch.load(model_path, map_location=device)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
        
        print("✅ Model loaded successfully!")
        
        # Test with dummy input
        print("🧪 Testing with dummy input...")
        dummy_input = torch.randn(1, 3, 224, 224)
        
        with torch.no_grad():
            output = model(dummy_input)
            probs = torch.nn.functional.softmax(output, dim=1)
            pred = torch.argmax(probs, dim=1).item()
            confidence = probs[0][pred].item()
        
        print(f"✅ Model inference successful!")
        print(f"   Prediction: {'DR' if pred == 0 else 'NoDR'}")
        print(f"   Confidence: {confidence:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return False

def test_dependencies():
    """Test if required packages are available."""
    print("\n🔍 Testing dependencies...")
    
    try:
        import gradio
        print("✅ Gradio imported successfully")
    except ImportError:
        print("❌ Gradio not found. Install with: pip install gradio")
        return False
    
    try:
        import PIL
        print("✅ PIL/Pillow imported successfully")
    except ImportError:
        print("❌ PIL/Pillow not found. Install with: pip install pillow")
        return False
    
    try:
        import numpy
        print("✅ NumPy imported successfully")
    except ImportError:
        print("❌ NumPy not found. Install with: pip install numpy")
        return False
    
    try:
        from pytorch_grad_cam import GradCAM
        print("✅ PyTorch Grad-CAM imported successfully")
    except ImportError:
        print("❌ PyTorch Grad-CAM not found. Install with: pip install pytorch-grad-cam")
        return False
    
    return True

def main():
    """Main test function."""
    print("🚀 Diabetic Retinopathy Detection - Model Test")
    print("=" * 50)
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    if not deps_ok:
        print("\n❌ Dependency test failed. Please install missing packages.")
        return
    
    # Test model loading
    model_ok = test_model_loading()
    
    print("\n" + "=" * 50)
    if model_ok:
        print("🎉 All tests passed! The app should work correctly.")
        print("   You can now run: python app.py")
    else:
        print("❌ Model test failed. Please check the error messages above.")
        print("   Make sure the model file is correct and all dependencies are installed.")

if __name__ == "__main__":
    main()
