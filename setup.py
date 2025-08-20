#!/usr/bin/env python3
"""
Setup script for Diabetic Retinopathy Detection App
Helps with installation and environment setup
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected. Python 3.8+ is required.")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible!")
    return True

def check_pip():
    """Check if pip is available."""
    print("📦 Checking pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip is available!")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip not found. Please install pip first.")
        return False

def upgrade_pip():
    """Upgrade pip to latest version."""
    print("🔄 Upgrading pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True)
        print("✅ pip upgraded successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not upgrade pip: {e}")
        return False

def install_requirements():
    """Install required packages from requirements.txt."""
    print("📥 Installing required packages...")
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_model_file():
    """Check if the model file exists."""
    print("🤖 Checking model file...")
    if os.path.exists("resnet50_dr_classifier.pth"):
        file_size = os.path.getsize("resnet50_dr_classifier.pth") / (1024 * 1024)
        print(f"✅ Model file found: resnet50_dr_classifier.pth ({file_size:.2f} MB)")
        return True
    else:
        print("❌ Model file 'resnet50_dr_classifier.pth' not found!")
        print("   Please ensure the model file is in the current directory.")
        return False

def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    
    directories = ["saved_predictions", "batch_results"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✅ Created: {directory}/")
        else:
            print(f"   📁 Exists: {directory}/")

def test_imports():
    """Test if all required packages can be imported."""
    print("🧪 Testing imports...")
    
    required_packages = [
        ("torch", "PyTorch"),
        ("torchvision", "TorchVision"),
        ("PIL", "Pillow"),
        ("numpy", "NumPy"),
        ("gradio", "Gradio"),
        ("pytorch_grad_cam", "PyTorch Grad-CAM")
    ]
    
    all_good = True
    
    for package, name in required_packages:
        try:
            if package == "PIL":
                import PIL
                print(f"   ✅ {name} imported successfully")
            else:
                __import__(package)
                print(f"   ✅ {name} imported successfully")
        except ImportError:
            print(f"   ❌ {name} import failed")
            all_good = False
    
    return all_good

def run_test():
    """Run the test script to verify everything works."""
    print("🧪 Running model test...")
    try:
        result = subprocess.run([sys.executable, "test_model.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Model test passed!")
            return True
        else:
            print("❌ Model test failed!")
            print("Output:", result.stdout)
            print("Errors:", result.stderr)
            return False
    except Exception as e:
        print(f"❌ Could not run test: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Diabetic Retinopathy Detection - Setup")
    print("=" * 50)
    
    # Check system info
    print(f"💻 System: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.executable}")
    print()
    
    # Step 1: Check Python version
    if not check_python_version():
        return False
    
    # Step 2: Check pip
    if not check_pip():
        return False
    
    # Step 3: Upgrade pip
    upgrade_pip()
    
    # Step 4: Install requirements
    if not install_requirements():
        return False
    
    # Step 5: Check model file
    if not check_model_file():
        return False
    
    # Step 6: Create directories
    create_directories()
    
    # Step 7: Test imports
    if not test_imports():
        print("❌ Some packages failed to import. Please check the installation.")
        return False
    
    # Step 8: Run test
    if not run_test():
        print("❌ Model test failed. Please check the model file and installation.")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Run the web app: python app.py")
    print("   2. Open your browser to the URL shown in the terminal")
    print("   3. Upload OCT images for analysis")
    print("\n🔄 For batch processing:")
    print("   python batch_process.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
