"""
Hugging Face Space Entry Point
AI Image Analysis Platform - Professional Edition
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set Hugging Face Space flag
os.environ['IS_HUGGINGFACE_SPACE'] = 'true'

# Import and run the professional edition
if __name__ == "__main__":
    try:
        from app_pro import main
        print("🚀 Launching AI Image Analysis Platform - Professional Edition")
        print("📍 Running on Hugging Face Space")
        main()
    except ImportError as e:
        print(f"❌ Error importing app_pro: {e}")
        print("Attempting to run standard edition...")
        try:
            from app_enhanced import main
            print("🚀 Launching AI Image Analysis Platform - Standard Edition")
            main()
        except ImportError as e2:
            print(f"❌ Error importing app_enhanced: {e2}")
            print("Please check your installation and dependencies.")
            sys.exit(1)
