# 🚀 Image AI Platform - Next Level Edition

An advanced local AI platform that combines **OCR**, **AI Image Captioning**, **Multi-language Translation**, and **Text-to-Speech** - all in one powerful application!

## ✨ Features

### 🔍 OCR (Optical Character Recognition)
- **Multi-language Support**: Extract text from images in English, Hindi, Kannada, Tamil, Telugu, Marathi, Bengali, and more
- **Powered by EasyOCR**: Deep learning-based OCR with high accuracy
- **Image Enhancement**: Adjust brightness, contrast, and sharpness for better text extraction

### 🎨 AI Image Captioning
- **BLIP Model Integration**: Generate natural language descriptions of images using Salesforce's BLIP model
- **Dual Mode Operation**:
  - **Local Mode**: Run the model on your machine for complete privacy
  - **Cloud Mode**: Use Hugging Face API for faster processing
- **Smart AI**: Understands complex scenes and generates detailed captions

### 🌍 Multi-Language Translation
- **19 Languages Supported**: English, Hindi, Kannada, Tamil, Telugu, Marathi, Bengali, Gujarati, Malayalam, Spanish, French, German, Italian, Portuguese, Japanese, Korean, Chinese, Russian, Arabic
- **Google Translator**: Powered by deep-translator for accurate translations
- **Translate Anything**: OCR text, AI captions, or any extracted content

### 🎧 Advanced Text-to-Speech
- **Native Voice Support**: Uses system voices for natural-sounding speech
  - **macOS**: Leverages the built-in `say` command with high-quality voices
  - **Other Platforms**: Uses pyttsx3 for cross-platform compatibility
- **Multi-Language Voices**: Automatic voice selection based on language
- **Customizable**: Adjust speech rate from slow to fast
- **Voice Preview**: See which voice is selected for each language

### 📥 Download Everything
- Download extracted text as TXT files
- Download AI-generated captions
- Download translations in any language
- Download audio files in WAV format
- All with timestamps for easy organization

### 🎨 Modern UI/UX
- **Tab-based Interface**: Organized sections for OCR, Caption, Translation, and TTS
- **Responsive Design**: Works beautifully on all screen sizes
- **Visual Feedback**: Progress indicators, success messages, and helpful tips
- **Statistics Dashboard**: Word count, character count, and usage metrics
- **Custom Styling**: Beautiful gradients and modern design elements

## 🛠️ Technologies Used

- **Frontend/UI**: Streamlit (Enhanced with custom CSS)
- **OCR Engine**: EasyOCR with multi-language support
- **AI Captioning**: Salesforce BLIP Model via Hugging Face Transformers
- **Translation**: Deep Translator (Google Translate API)
- **Text-to-Speech**: 
  - macOS: Native `say` command
  - Cross-platform: pyttsx3
- **Image Processing**: PIL (Pillow), OpenCV
- **Deep Learning**: PyTorch, Transformers
- **Deployment Ready**: Optimized for local and cloud deployment

## 📋 Prerequisites

- Python 3.8 or higher
- 4GB+ RAM (8GB recommended for local AI captioning)
- macOS, Windows, or Linux

## 🚀 Installation

1. **Clone or download this repository**

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   Note: For AI captioning in local mode, PyTorch and Transformers will download the BLIP model (~1GB) on first use.

3. **Verify installation:**

   ```bash
   python3 -c "import streamlit, easyocr, torch, transformers; print('✅ All packages installed!')"
   ```

## 💻 Usage

### Quick Start

Run the application using the provided script:

```bash
./run.sh
```

Or manually:

```bash
python3 -m streamlit run src/app_enhanced.py
```

### Using the Application

1. **Select Image Source**:
   - **Upload from Device**: Click "Upload from Device" and select a JPG, PNG, or other image file
   - **Use Sample Image**: Select from pre-loaded sample images in the dropdown

2. **Explore Tabs**:
   - **📸 Image & OCR**: View your image and extract text
   - **🎨 AI Caption**: Generate AI descriptions of your image
   - **🌍 Translation**: Translate extracted text or captions to 19 languages
   - **🎧 Text-to-Speech**: Convert any text to natural-sounding audio

3. **Customize Settings** (Sidebar):
   - Select OCR languages
   - Enable/disable AI captioning
   - Choose between local or cloud mode for captions
   - Adjust image enhancement (brightness, contrast, sharpness)

4. **Download Results**:
   - Every feature includes a download button
   - Get TXT files for text, captions, and translations
   - Get WAV files for audio

### Sample Images

The application includes 5 sample images for quick testing:
- `sample_1_english.jpg` - English text
- `sample_2_hindi.jpg` - Hindi text
- `sample_3_mixed.jpg` - Mixed language text
- `sample_4_document.jpg` - Document/Invoice
- `sample_5_menu.jpg` - Menu card

You can add your own sample images to the `sample_images/` folder.

### Tips for Best Results

- **For Better OCR**: Enable image enhancement and adjust brightness/contrast
- **For Faster Captions**: Use Cloud API mode (requires internet)
- **For Privacy**: Use Local Mode for all features (no internet required)
- **For Clear Audio**: Select a voice that matches your text language

## 📁 Project Structure

```
Image Ai/
├── src/
│   ├── app_enhanced.py       # Main enhanced application
│   ├── app.py                # Original simple version
│   ├── ocr_engine.py         # OCR functionality
│   ├── caption_engine.py     # AI captioning (NEW)
│   ├── translation_engine.py # Translation (NEW)
│   └── tts_engine.py         # Text-to-Speech
├── requirements.txt          # Python dependencies
├── run.sh                    # Launch script
└── README.md                # This file
```

## 🎯 Use Cases

- **Education**: Extract text from textbooks, notes, and study material
- **Accessibility**: Convert documents to speech for visually impaired users
- **Content Creation**: Generate captions for blogs, portfolios, and social media
- **Translation on the go**: Understand multilingual signage or documents instantly
- **Research & Archiving**: Digitize old manuscripts and annotate them with captions
- **Language Learning**: Listen to translated text in native accents

## 🌟 Why This Stands Out

- ✅ Runs fully offline (privacy-first) or optionally uses cloud captioning for speed
- ✅ Combines OCR, captioning, translation, and TTS in one streamlined UI
- ✅ Modern Streamlit experience with tabs, stats, and download actions
- ✅ Highly customizable—add languages, voices, or new AI models easily

## 🔧 Advanced Configuration

### Hugging Face API Token (optional)
1. Create an access token at Hugging Face.
2. In `src/caption_engine.py`, set `headers = {"Authorization": f"Bearer {API_TOKEN}"}` before calling the API.

### Add More Translation Languages
Edit the `supported_languages` dictionary inside `src/translation_engine.py` to include the new language name and code.

## 📊 Performance Notes

| Feature | Local Mode | Cloud Mode |
| --- | --- | --- |
| OCR | 2-5s | N/A |
| Captioning | 5-10s (first run downloads model) | 1-3s |
| Translation | 0.5-2s | 0.5-2s |
| Text-to-Speech | 1-3s / 100 words | 1-3s / 100 words |

## 🐛 Troubleshooting

- **"Error initializing engines"**: reinstall requirements and ensure torch supports your hardware.
- **"Caption model slow"**: first run fetches ~1GB weights; reuse sessions to avoid reloads.
- **"Audio not playing"**: on macOS ensure `say` works; on Windows/Linux ensure speakers default device.
- **"Translation failed"**: verify internet connection; Google Translator needs network access.

## 🙏 Credits

- EasyOCR, Salesforce BLIP, Deep Translator, Streamlit, Hugging Face transformers
- Inspired by [Mohammed Saqhib's Image Caption AI](https://github.com/Mohammed-Saqhib/Image-Caption-Ai)

---

Built with ❤️ as a next-level Final Year Project.
