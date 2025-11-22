import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

def test_imports():
    print("Testing imports...")
    try:
        import streamlit
        import easyocr
        import pyttsx3
        print("✅ Imports successful")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        sys.exit(1)

def test_ocr():
    print("\nTesting OCR Engine initialization (this might take a while to download models)...")
    try:
        from ocr_engine import OCREngine
        # Initialize with English only for speed
        ocr = OCREngine(languages=['en'])
        print("✅ OCR Engine initialized")
    except Exception as e:
        print(f"❌ OCR Engine failed: {e}")
        # Don't exit, try TTS

def test_tts():
    print("\nTesting TTS Engine initialization...")
    try:
        from tts_engine import TTSEngine
        tts = TTSEngine()
        voices = tts.get_voices()
        print(f"✅ TTS Engine initialized. Found {len(voices)} voices.")
    except Exception as e:
        print(f"❌ TTS Engine failed: {e}")

if __name__ == "__main__":
    print("Starting System Check...")
    test_imports()
    test_ocr()
    test_tts()
    print("\nSystem Check Complete.")
