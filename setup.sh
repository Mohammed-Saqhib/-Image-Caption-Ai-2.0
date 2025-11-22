#!/bin/bash

# Quick Setup Script for AI Image Analysis Platform
# This script automates the initial setup process

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     AI Image Analysis Platform - Quick Setup              ║"
echo "║     Professional Edition Setup Script                     ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to print status messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check Python version
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
print_success "Python $PYTHON_VERSION found"

# Check Python version is 3.8+
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d '.' -f 1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d '.' -f 2)
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    print_error "Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Check if pip is installed
print_status "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip."
    exit 1
fi
print_success "pip3 found"

# Ask user for installation type
echo ""
echo -e "${YELLOW}Select installation type:${NC}"
echo "1) Quick install (recommended)"
echo "2) Development install (includes dev tools)"
echo "3) Minimal install (basic features only)"
read -p "Enter choice [1-3]: " INSTALL_TYPE

# Create virtual environment
echo ""
print_status "Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip --quiet
print_success "pip upgraded"

# Install requirements based on choice
echo ""
case $INSTALL_TYPE in
    1)
        print_status "Installing dependencies (Quick install)..."
        pip install -r requirements.txt --quiet
        ;;
    2)
        print_status "Installing dependencies (Development install)..."
        pip install -r requirements.txt --quiet
        # Install dev tools
        print_status "Installing development tools..."
        pip install pytest pytest-cov black flake8 mypy --quiet
        ;;
    3)
        print_status "Installing dependencies (Minimal install)..."
        # Install only essential packages
        pip install streamlit easyocr pillow opencv-python numpy --quiet
        ;;
    *)
        print_error "Invalid choice. Exiting."
        exit 1
        ;;
esac
print_success "Dependencies installed successfully"

# Create necessary directories
echo ""
print_status "Creating necessary directories..."
mkdir -p cache models output uploads
print_success "Directories created"

# Download sample images if not present
if [ ! -d "sample_images" ] || [ -z "$(ls -A sample_images)" ]; then
    print_status "Sample images directory is empty. Please add sample images."
else
    print_success "Sample images found"
fi

# Test installation
echo ""
print_status "Testing installation..."
python3 -c "import streamlit, easyocr, PIL, cv2; print('✅ All core packages imported successfully')" && \
    print_success "Installation test passed" || \
    print_error "Installation test failed"

# Ask if user wants to run demo
echo ""
read -p "Would you like to run the demo now? (y/n): " RUN_DEMO
if [ "$RUN_DEMO" = "y" ] || [ "$RUN_DEMO" = "Y" ]; then
    print_status "Running demo..."
    python3 demo.py
fi

# Display next steps
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗"
echo "║                    Setup Complete! 🎉                      ║"
echo "╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Activate virtual environment:"
echo -e "   ${YELLOW}source venv/bin/activate${NC}"
echo ""
echo "2. Run the application:"
echo -e "   ${YELLOW}./run_pro.sh pro${NC}  (Professional Edition)"
echo -e "   ${YELLOW}./run.sh${NC}          (Standard Edition)"
echo ""
echo "3. Access the application:"
echo -e "   ${YELLOW}http://localhost:8501${NC}"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "   • README.md - Main documentation"
echo "   • README_PRO.md - Professional features"
echo "   • HUGGINGFACE_DEPLOYMENT.md - Deployment guide"
echo ""
echo -e "${BLUE}Need help?${NC}"
echo "   • Check TESTING_GUIDE.md"
echo "   • Visit GitHub Issues"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
