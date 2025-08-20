# 🚀 Quick Start Guide

## ⚡ Get Running in 5 Minutes

### 1. **Prerequisites Check**
- ✅ Python 3.8+ installed
- ✅ Model file `resnet50_dr_classifier.pth` present
- ✅ Internet connection (for first-time package installation)

### 2. **Easy Setup (Windows)**
```bash
# Option A: Double-click the batch file
run_app.bat

# Option B: Use PowerShell
.\run_app.ps1

# Option C: Use PowerShell with setup
.\run_app.ps1 -Setup
```

### 3. **Manual Setup (All Platforms)**
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test the setup
python test_model.py

# Run the app
python app.py
```

### 4. **What Happens Next**
- 🌐 Web interface opens at `http://127.0.0.1:7860`
- 📁 Upload OCT images for analysis
- 🤖 AI classifies images as DR or NoDR
- 🔥 Grad-CAM heatmap shows AI focus areas
- 💾 Results automatically saved to `saved_predictions/` folder

## 🎯 Usage Examples

### **Single Image Analysis**
1. Open `http://127.0.0.1:7860` in your browser
2. Upload an OCT image
3. View results and Grad-CAM visualization

### **Batch Processing**
```bash
python batch_process.py
```
- Process multiple images at once
- Get CSV report with all results
- Grad-CAM images saved to `batch_results/` folder

### **Testing & Validation**
```bash
python test_model.py
```
- Verify model loading
- Test basic functionality
- Check all dependencies

## 🔧 Troubleshooting

### **Common Issues**

| Problem | Solution |
|---------|----------|
| "Model file not found" | Ensure `resnet50_dr_classifier.pth` is in the project folder |
| "Package not found" | Run `pip install -r requirements.txt` |
| "CUDA errors" | App runs on CPU by default. GPU not required |
| "Port already in use" | Change port in `config.py` or kill existing process |

### **Get Help**
- Run `python setup.py` for comprehensive setup
- Check `README.md` for detailed documentation
- Use `python test_model.py` to diagnose issues

## 📁 Project Structure
```
Deep_Learning_for_Ophthalmologist/
├── app.py                          # 🌐 Main web application
├── batch_process.py                # 🔄 Batch processing script
├── test_model.py                   # 🧪 Testing and validation
├── setup.py                        # ⚙️  Automated setup
├── config.py                       # 🔧 Configuration settings
├── requirements.txt                # 📦 Python dependencies
├── resnet50_dr_classifier.pth     # 🤖 AI model weights
├── run_app.bat                     # 🪟 Windows batch launcher
├── run_app.ps1                     # 🪟 Windows PowerShell launcher
├── README.md                       # 📚 Complete documentation
├── QUICK_START.md                  # 🚀 This quick start guide
├── saved_predictions/              # 💾 Single image results
└── batch_results/                  # 📊 Batch processing results
```

## 🎉 You're Ready!

Your AI-powered diabetic retinopathy detection app is now ready to use! 

**Next steps:**
1. 🖱️ Double-click `run_app.bat` (Windows) or run `python app.py`
2. 🌐 Open your web browser to the displayed URL
3. 📁 Upload OCT images for analysis
4. 🔬 Explore the Grad-CAM visualizations
5. 📊 Use batch processing for multiple images

**Remember:** This tool is for research and educational purposes. Always consult healthcare professionals for medical diagnosis.

---

*Need help? Check the full `README.md` or run `python setup.py` for detailed assistance.*
