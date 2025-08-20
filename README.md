# AI Diabetic Retinopathy Detection

An AI-powered application for detecting diabetic retinopathy (DR) from Optical Coherence Tomography (OCT) images using deep learning and Grad-CAM visualization.

## 🏥 What is Diabetic Retinopathy?

Diabetic retinopathy is a diabetes complication that affects the eyes. It's caused by damage to the blood vessels of the light-sensitive tissue at the back of the eye (retina). Early detection is crucial for preventing vision loss.

## 🚀 Features

- **AI Classification**: Uses a pre-trained ResNet-50 model to classify OCT images as DR (Diabetic Retinopathy) or NoDR (No Diabetic Retinopathy)
- **Grad-CAM Visualization**: Shows which areas of the image the AI focuses on for diagnosis
- **Confidence Scoring**: Provides probability scores for predictions
- **Image Storage**: Automatically saves analyzed images with timestamps
- **Web Interface**: User-friendly Gradio web interface

## 📋 Requirements

- Python 3.8 or higher
- PyTorch 2.0+
- CUDA-compatible GPU (optional, for faster inference)

## 🛠️ Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd Deep_Learning_for_Ophthalmologist
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to the URL shown in the terminal (usually `http://127.0.0.1:7860`)

3. **Upload an OCT image** by clicking the upload area or dragging and dropping an image file

4. **View results**:
   - The AI will analyze the image and show the classification result
   - A Grad-CAM heatmap will highlight areas of interest
   - The prediction and confidence score will be displayed
   - The analyzed image will be automatically saved to the `saved_predictions` folder

## 📁 File Structure

```
Deep_Learning_for_Ophthalmologist/
├── app.py                          # Main application file
├── requirements.txt                # Python dependencies
├── resnet50_dr_classifier.pth     # Pre-trained model weights
├── README.md                      # This file
└── saved_predictions/             # Folder for saved analyzed images
```

## 🔬 How It Works

1. **Image Preprocessing**: OCT images are resized to 224x224 pixels and normalized
2. **AI Analysis**: A ResNet-50 model processes the image to classify DR vs NoDR
3. **Grad-CAM**: Generates a heatmap showing which image regions influenced the AI's decision
4. **Results**: Displays classification, confidence score, and visual heatmap

## 📊 Model Information

- **Architecture**: ResNet-50 with modified final layer for binary classification
- **Training**: Pre-trained on OCT image dataset
- **Classes**: 2 (DR - Diabetic Retinopathy, NoDR - No Diabetic Retinopathy)
- **Input**: 224x224 RGB images
- **Output**: Binary classification with confidence scores

## ⚠️ Important Notes

- **Medical Disclaimer**: This tool is for research and educational purposes only. It should not be used for actual medical diagnosis without proper validation and clinical oversight.
- **Image Quality**: For best results, use high-quality OCT images with good contrast and resolution
- **Model Limitations**: The model's accuracy depends on the quality and characteristics of the training data

## 🐛 Troubleshooting

- **CUDA errors**: The app runs on CPU by default. If you have GPU issues, ensure PyTorch is installed correctly
- **Memory issues**: Large images may cause memory problems. The app automatically resizes images to 224x224
- **Model loading errors**: Ensure `resnet50_dr_classifier.pth` is in the same directory as `app.py`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is for educational and research purposes. Please ensure compliance with relevant regulations when using medical imaging data.

## 🔗 References

- [PyTorch](https://pytorch.org/)
- [Gradio](https://gradio.app/)
- [Grad-CAM](https://github.com/jacobgil/pytorch-grad-cam)
- [ResNet Paper](https://arxiv.org/abs/1512.03385)

---

**Note**: This application is designed for research and educational purposes in ophthalmology and medical AI. Always consult with qualified healthcare professionals for actual medical diagnosis and treatment decisions.