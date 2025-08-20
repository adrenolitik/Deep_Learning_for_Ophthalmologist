#!/usr/bin/env python3
"""
Batch processing script for diabetic retinopathy detection.
Processes multiple OCT images and saves results in a structured format.
"""

import os
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
from torchvision import models, transforms
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
import csv
import datetime
from pathlib import Path

class BatchDRDetector:
    def __init__(self, model_path="resnet50_dr_classifier.pth"):
        """Initialize the batch detector with the trained model."""
        self.device = torch.device("cpu")
        self.model_path = model_path
        self.model = None
        self.cam = None
        self.transform = None
        self.output_dir = "batch_results"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        self._load_model()
        self._setup_gradcam()
        self._setup_transforms()
    
    def _load_model(self):
        """Load the trained ResNet-50 model."""
        print("🔄 Loading model...")
        try:
            self.model = models.resnet50(weights=None)
            self.model.fc = torch.nn.Linear(self.model.fc.in_features, 2)
            self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def _setup_gradcam(self):
        """Setup Grad-CAM for visualization."""
        target_layer = self.model.layer4[-1]
        self.cam = GradCAM(model=self.model, target_layers=[target_layer])
        print("✅ Grad-CAM setup complete!")
    
    def _setup_transforms(self):
        """Setup image preprocessing transforms."""
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    
    def process_single_image(self, image_path):
        """Process a single image and return results."""
        try:
            # Load and preprocess image
            img = Image.open(image_path).convert("RGB")
            img_tensor = self.transform(img).unsqueeze(0).to(self.device)
            
            # Get prediction
            with torch.no_grad():
                output = self.model(img_tensor)
                probs = F.softmax(output, dim=1)
                pred = torch.argmax(probs, dim=1).item()
                confidence = probs[0][pred].item()
            
            # Generate Grad-CAM
            rgb_img_np = np.array(img.resize((224, 224))).astype(np.float32) / 255.0
            rgb_img_np = np.ascontiguousarray(rgb_img_np)
            grayscale_cam = self.cam(input_tensor=img_tensor, targets=[ClassifierOutputTarget(pred)])[0]
            cam_image = show_cam_on_image(rgb_img_np, grayscale_cam, use_rgb=True)
            
            # Determine label
            label = "DR" if pred == 0 else "NoDR"
            
            return {
                'image_path': image_path,
                'prediction': label,
                'confidence': confidence,
                'dr_probability': 1 - confidence if pred == 1 else confidence,
                'cam_image': cam_image,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'image_path': image_path,
                'prediction': 'ERROR',
                'confidence': 0.0,
                'dr_probability': 0.0,
                'cam_image': None,
                'status': f'error: {str(e)}'
            }
    
    def process_directory(self, input_dir, extensions=['.jpg', '.jpeg', '.png', '.tiff', '.bmp']):
        """Process all images in a directory."""
        print(f"🔍 Scanning directory: {input_dir}")
        
        # Find all image files
        image_files = []
        for ext in extensions:
            image_files.extend(Path(input_dir).glob(f"*{ext}"))
            image_files.extend(Path(input_dir).glob(f"*{ext.upper()}"))
        
        if not image_files:
            print("❌ No image files found in the directory!")
            return []
        
        print(f"📁 Found {len(image_files)} image files")
        
        # Process each image
        results = []
        for i, image_path in enumerate(image_files, 1):
            print(f"🔄 Processing {i}/{len(image_files)}: {image_path.name}")
            result = self.process_single_image(str(image_path))
            results.append(result)
            
            # Save Grad-CAM image if successful
            if result['status'] == 'success' and result['cam_image'] is not None:
                cam_filename = f"cam_{Path(image_path).stem}_{result['prediction']}_{result['confidence']:.3f}.png"
                cam_path = os.path.join(self.output_dir, cam_filename)
                Image.fromarray(result['cam_image']).save(cam_path)
                result['cam_saved_path'] = cam_path
        
        return results
    
    def save_results_csv(self, results, filename=None):
        """Save results to a CSV file."""
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dr_results_{timestamp}.csv"
        
        csv_path = os.path.join(self.output_dir, filename)
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['image_path', 'prediction', 'confidence', 'dr_probability', 'status', 'cam_saved_path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in results:
                # Clean up the result dict for CSV
                csv_result = {k: v for k, v in result.items() if k in fieldnames}
                writer.writerow(csv_result)
        
        print(f"📊 Results saved to: {csv_path}")
        return csv_path
    
    def generate_summary(self, results):
        """Generate a summary of the batch processing results."""
        successful = [r for r in results if r['status'] == 'success']
        errors = [r for r in results if r['status'] != 'success']
        
        if successful:
            dr_count = len([r for r in successful if r['prediction'] == 'DR'])
            nodr_count = len([r for r in successful if r['prediction'] == 'NoDR'])
            
            avg_confidence = np.mean([r['confidence'] for r in successful])
            avg_dr_prob = np.mean([r['dr_probability'] for r in successful])
            
            summary = {
                'total_images': len(results),
                'successful': len(successful),
                'errors': len(errors),
                'dr_detected': dr_count,
                'no_dr_detected': nodr_count,
                'dr_percentage': (dr_count / len(successful)) * 100 if successful else 0,
                'average_confidence': avg_confidence,
                'average_dr_probability': avg_dr_prob
            }
        else:
            summary = {
                'total_images': len(results),
                'successful': 0,
                'errors': len(errors),
                'dr_detected': 0,
                'no_dr_detected': 0,
                'dr_percentage': 0,
                'average_confidence': 0,
                'average_dr_probability': 0
            }
        
        return summary

def main():
    """Main function for batch processing."""
    print("🚀 Diabetic Retinopathy Detection - Batch Processing")
    print("=" * 60)
    
    # Check if model exists
    if not os.path.exists("resnet50_dr_classifier.pth"):
        print("❌ Model file 'resnet50_dr_classifier.pth' not found!")
        print("   Please ensure the model file is in the current directory.")
        return
    
    # Initialize detector
    try:
        detector = BatchDRDetector()
    except Exception as e:
        print(f"❌ Failed to initialize detector: {e}")
        return
    
    # Get input directory from user
    print("\n📁 Enter the path to the directory containing OCT images:")
    print("   (or press Enter to use current directory)")
    
    user_input = input("Directory path: ").strip()
    
    if user_input:
        input_dir = user_input
    else:
        input_dir = os.getcwd()
    
    if not os.path.exists(input_dir):
        print(f"❌ Directory not found: {input_dir}")
        return
    
    print(f"\n🎯 Processing images from: {input_dir}")
    
    # Process images
    results = detector.process_directory(input_dir)
    
    if not results:
        print("❌ No results to process!")
        return
    
    # Save results
    csv_path = detector.save_results_csv(results)
    
    # Generate and display summary
    summary = detector.generate_summary(results)
    
    print("\n📊 Batch Processing Summary")
    print("=" * 40)
    print(f"Total images: {summary['total_images']}")
    print(f"Successfully processed: {summary['successful']}")
    print(f"Errors: {summary['errors']}")
    
    if summary['successful'] > 0:
        print(f"DR detected: {summary['dr_detected']} ({summary['dr_percentage']:.1f}%)")
        print(f"No DR detected: {summary['no_dr_detected']}")
        print(f"Average confidence: {summary['average_confidence']:.3f}")
        print(f"Average DR probability: {summary['average_dr_probability']:.3f}")
    
    print(f"\n📁 Results saved to: {detector.output_dir}/")
    print(f"📊 CSV report: {csv_path}")

if __name__ == "__main__":
    main()
