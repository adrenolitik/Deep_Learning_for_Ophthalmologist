#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Launcher script for Diabetic Retinopathy Detection App
    
.DESCRIPTION
    This script checks prerequisites and launches the AI-powered
    diabetic retinopathy detection application.
    
.PARAMETER Setup
    Run setup instead of launching the app
    
.PARAMETER Test
    Run tests instead of launching the app
    
.PARAMETER Batch
    Launch batch processing instead of the web app
#>

param(
    [switch]$Setup,
    [switch]$Test,
    [switch]$Batch
)

# Set console title
$Host.UI.RawUI.WindowTitle = "Diabetic Retinopathy Detection App"

# Function to write colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Function to check Python installation
function Test-PythonInstallation {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Python found: $pythonVersion" "Green"
            return $true
        }
    }
    catch {
        Write-ColorOutput "❌ Python not found in PATH" "Red"
        return $false
    }
    return $false
}

# Function to check model file
function Test-ModelFile {
    $modelPath = "resnet50_dr_classifier.pth"
    if (Test-Path $modelPath) {
        $fileSize = (Get-Item $modelPath).Length / 1MB
        Write-ColorOutput "✅ Model file found: $modelPath ($([math]::Round($fileSize, 2)) MB)" "Green"
        return $true
    }
    else {
        Write-ColorOutput "❌ Model file not found: $modelPath" "Red"
        return $false
    }
}

# Function to activate virtual environment
function Activate-VirtualEnvironment {
    $venvPath = "venv\Scripts\Activate.ps1"
    if (Test-Path $venvPath) {
        Write-ColorOutput "🔄 Activating virtual environment..." "Yellow"
        & $venvPath
        return $true
    }
    else {
        Write-ColorOutput "ℹ️  No virtual environment found. Using system Python." "Cyan"
        return $false
    }
}

# Function to run setup
function Start-Setup {
    Write-ColorOutput "🚀 Running setup..." "Yellow"
    if (Test-PythonInstallation) {
        python setup.py
    }
    else {
        Write-ColorOutput "❌ Cannot run setup without Python" "Red"
    }
}

# Function to run tests
function Start-Tests {
    Write-ColorOutput "🧪 Running tests..." "Yellow"
    if (Test-PythonInstallation) {
        python test_model.py
    }
    else {
        Write-ColorOutput "❌ Cannot run tests without Python" "Red"
    }
}

# Function to start batch processing
function Start-BatchProcessing {
    Write-ColorOutput "🔄 Starting batch processing..." "Yellow"
    if (Test-PythonInstallation) {
        python batch_process.py
    }
    else {
        Write-ColorOutput "❌ Cannot start batch processing without Python" "Red"
    }
}

# Function to start web app
function Start-WebApp {
    Write-ColorOutput "🌐 Starting web application..." "Yellow"
    if (Test-PythonInstallation) {
        python app.py
    }
    else {
        Write-ColorOutput "❌ Cannot start web app without Python" "Red"
    }
}

# Main execution
Clear-Host
Write-ColorOutput "========================================" "Cyan"
Write-ColorOutput "  Diabetic Retinopathy Detection App" "Cyan"
Write-ColorOutput "========================================" "Cyan"
Write-Host ""

# Check Python installation
if (-not (Test-PythonInstallation)) {
    Write-ColorOutput "❌ Python is not installed or not in PATH" "Red"
    Write-ColorOutput "Please install Python 3.8+ and try again" "Yellow"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check model file
if (-not (Test-ModelFile)) {
    Write-ColorOutput "❌ Model file is missing!" "Red"
    Write-ColorOutput "Please ensure the model file is in the current directory." "Yellow"
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment if available
Activate-VirtualEnvironment

Write-Host ""

# Determine what to run based on parameters
if ($Setup) {
    Start-Setup
}
elseif ($Test) {
    Start-Tests
}
elseif ($Batch) {
    Start-BatchProcessing
}
else {
    # Default: start web app
    Write-ColorOutput "🎯 Starting web application..." "Green"
    Write-ColorOutput "The app will open in your web browser at: http://127.0.0.1:7860" "Cyan"
    Write-ColorOutput "Press Ctrl+C to stop the application" "Yellow"
    Write-Host ""
    
    Start-WebApp
}

Write-Host ""
Read-Host "Press Enter to exit"
