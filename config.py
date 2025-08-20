#!/usr/bin/env python3
"""
Configuration file for Diabetic Retinopathy Detection App
Modify these settings to customize the application behavior
"""

import os

# Model Configuration
MODEL_CONFIG = {
    'model_path': 'resnet50_dr_classifier.pth',
    'model_architecture': 'resnet50',
    'num_classes': 2,
    'input_size': (224, 224),
    'device': 'cpu'  # Change to 'cuda' if you have a GPU
}

# Image Processing Configuration
IMAGE_CONFIG = {
    'supported_formats': ['.jpg', '.jpeg', '.png', '.tiff', '.bmp'],
    'max_file_size_mb': 50,  # Maximum file size in MB
    'normalization_mean': [0.485, 0.456, 0.406],
    'normalization_std': [0.229, 0.224, 0.225]
}

# Grad-CAM Configuration
GRADCAM_CONFIG = {
    'target_layer': 'layer4[-1]',  # Target layer for visualization
    'colormap': 'jet',  # Colormap for heatmap visualization
    'alpha': 0.4  # Transparency of the heatmap overlay
}

# Application Configuration
APP_CONFIG = {
    'title': 'AI Diabetic Retinopathy Detection',
    'description': 'Upload an OCT image to analyze for diabetic retinopathy. The AI will show a Grad-CAM heatmap highlighting areas of interest.',
    'theme': 'default',  # Gradio theme
    'share': False,  # Whether to create a public link
    'server_name': '127.0.0.1',
    'server_port': 7860,
    'debug': False
}

# Output Configuration
OUTPUT_CONFIG = {
    'save_predictions': True,
    'save_gradcam': True,
    'output_dir': 'saved_predictions',
    'batch_output_dir': 'batch_results',
    'filename_format': '{timestamp}_{label}_{confidence:.3f}.png'
}

# Medical Disclaimer
MEDICAL_DISCLAIMER = """
⚠️ MEDICAL DISCLAIMER ⚠️

This tool is for research and educational purposes only. 
It should not be used for actual medical diagnosis without proper validation and clinical oversight.

Always consult with qualified healthcare professionals for medical diagnosis and treatment decisions.
"""

# Class Labels
CLASS_LABELS = {
    0: 'DR',      # Diabetic Retinopathy
    1: 'NoDR'     # No Diabetic Retinopathy
}

# Confidence Thresholds
CONFIDENCE_THRESHOLDS = {
    'high_confidence': 0.9,    # High confidence threshold
    'medium_confidence': 0.7,  # Medium confidence threshold
    'low_confidence': 0.5      # Low confidence threshold
}

# Logging Configuration
LOGGING_CONFIG = {
    'log_level': 'INFO',
    'log_file': 'dr_detection.log',
    'log_format': '%(asctime)s - %(levelname)s - %(message)s'
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'batch_size': 1,           # Batch size for processing
    'num_workers': 0,          # Number of worker processes
    'pin_memory': False,       # Pin memory for faster data transfer
    'prefetch_factor': 2       # Prefetch factor for data loading
}

def get_model_path():
    """Get the model path, checking if it exists."""
    model_path = MODEL_CONFIG['model_path']
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return model_path

def get_device():
    """Get the device to use for inference."""
    device = MODEL_CONFIG['device']
    if device == 'cuda' and not torch.cuda.is_available():
        print("⚠️  CUDA requested but not available. Falling back to CPU.")
        return 'cpu'
    return device

def get_output_directory():
    """Get the output directory, creating it if it doesn't exist."""
    output_dir = OUTPUT_CONFIG['output_dir']
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def get_batch_output_directory():
    """Get the batch output directory, creating it if it doesn't exist."""
    batch_dir = OUTPUT_CONFIG['batch_output_dir']
    os.makedirs(batch_dir, exist_ok=True)
    return batch_dir

# Import torch here to avoid circular imports
try:
    import torch
except ImportError:
    print("⚠️  PyTorch not available. Some functions may not work.")
    torch = None
