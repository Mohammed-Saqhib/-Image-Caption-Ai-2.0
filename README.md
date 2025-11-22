---
title: AI Image Analysis Platform
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.28.0"
app_file: app.py
pinned: false
license: mit
---

# 🚀 AI Image Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

<div align="center">
  <img src="https://img.shields.io/badge/AI-Powered-purple?style=for-the-badge" alt="AI Powered"/>
  <img src="https://img.shields.io/badge/OCR-Multi--Language-blue?style=for-the-badge" alt="Multi-Language OCR"/>
  <img src="https://img.shields.io/badge/TTS-Smart-orange?style=for-the-badge" alt="Smart TTS"/>
</div>

---

## 📖 Overview

A **comprehensive AI-powered platform** that transforms images into actionable content through cutting-edge machine learning. Extract text, generate captions, translate to 19 languages, and create natural-sounding audio - all in one unified interface.

Perfect for **accessibility**, **content creation**, **education**, **research**, and **business automation**.

### ✨ Key Highlights

🔍 **Multi-Language OCR** - Extract text from images in 7 languages  
🎨 **AI Image Captioning** - Generate descriptions using BLIP model  
🌍 **Translation** - Translate to 19 languages instantly  
🎧 **Smart Text-to-Speech** - Auto-translating TTS with natural voices  
⚡ **Batch Processing** - Process multiple images simultaneously  
📦 **Multi-Format Export** - PDF, DOCX, JSON, SRT, TXT, and ZIP  
🖼️ **Advanced Preprocessing** - Noise reduction, deskewing, enhancement  
📊 **Quality Assessment** - Real-time image quality scoring  

---

## 🎯 Live Demo

### Try it now:
- **🤗 Hugging Face Space**: [Coming Soon - Deploy your fork here!]
- **💻 Local Demo**: Run `./run_pro.sh pro` after installation

### Quick Preview

```bash
# Clone and run in 3 commands
git clone https://github.com/YOUR_USERNAME/Image-AI-Platform.git
cd Image-AI-Platform
pip install -r requirements.txt && ./run_pro.sh pro
```

---

## 🌟 Features

<table>
<tr>
<td width="50%">

### 📝 OCR Engine
- **7 Languages**: English, Hindi, Kannada, Tamil, Telugu, Marathi, Bengali
- **High Accuracy**: EasyOCR with deep learning
- **Image Enhancement**: Brightness, contrast, sharpness adjustments
- **Confidence Scoring**: Quality metrics for extracted text
- **Multiple Formats**: TXT, JSON, PDF, DOCX exports

</td>
<td width="50%">

### 🎨 AI Captioning
- **BLIP Model**: State-of-the-art image understanding
- **Dual Modes**: Local processing or Cloud API
- **Customizable**: Adjust caption length and detail
- **Fast**: 1-7 seconds depending on mode
- **Accurate**: Context-aware descriptions

</td>
</tr>
<tr>
<td width="50%">

### 🌐 Translation
- **19 Languages**: Major world languages supported
- **Google Translate**: Powered by Deep Translator
- **Context Preserved**: Maintains formatting
- **SRT Subtitles**: Export for video captioning
- **Instant**: Sub-second translations

</td>
<td width="50%">

### 🎧 Smart TTS
- **Auto-Translation**: Text automatically translated to voice language
- **Natural Voices**: System voices for authentic pronunciation
- **9 Languages**: Including all major Indian languages
- **Adjustable Speed**: 100-300 words per minute
- **High Quality**: WAV format audio output

</td>
</tr>
</table>

### 🚀 Professional Edition Features

<details>
<summary><b>Click to expand advanced features</b></summary>

#### 🖼️ Image Preprocessing
- **Noise Reduction**: Remove image artifacts
- **Auto-Deskewing**: Straighten rotated documents
- **Adaptive Thresholding**: Optimize text contrast
- **Edge Enhancement**: Sharpen text boundaries
- **Contrast Stretching**: Improve visibility
- **Border Removal**: Clean document edges
- **Smart Upscaling**: Enhance resolution
- **Quality Presets**: Auto-enhance, custom, aggressive

#### 📊 Quality Assessment
- **Sharpness Score**: Measure text clarity
- **Brightness Analysis**: Optimal light detection
- **Contrast Measurement**: Text visibility rating
- **Overall Score**: 0-100% quality metric
- **Recommendations**: Auto-suggested improvements

#### ⚡ Batch Processing
- **Unlimited Images**: Process hundreds at once
- **Progress Tracking**: Live status updates
- **Comprehensive Reports**: Detailed batch analytics
- **ZIP Packages**: All results bundled
- **Selective Processing**: Choose OCR, caption, translate

#### 📦 Export Options
- **PDF**: Professional reports with metadata
- **DOCX**: Editable Word documents
- **JSON**: Structured data for developers
- **SRT**: Video subtitle files
- **TXT**: Plain text files
- **ZIP**: Complete batch packages

</details>

---

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **OS**: macOS, Linux, or Windows
- **Internet**: For cloud features (optional)

### Installation

#### Local Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Image-AI-Platform.git
cd Image-AI-Platform

# Install dependencies
pip install -r requirements.txt

# Run Standard Edition
./run.sh

# Or run Professional Edition
./run_pro.sh pro
```

#### Hugging Face Space Deployment

<details>
<summary><b>Deploy to Hugging Face in 5 minutes</b></summary>

1. **Fork this repository** to your GitHub account

2. **Create a new Space** on [Hugging Face](https://huggingface.co/spaces)
   - Select **Streamlit** as the SDK
   - Choose your hardware (CPU is sufficient)

3. **Link your GitHub repo** or upload files directly

4. **Create `app.py`** in the root directory:
   ```python
   # app.py - Hugging Face entry point
   import sys
   import os
   
   # Add src to path
   sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
   
   # Import and run the professional app
   from app_pro import main
   
   if __name__ == "__main__":
       main()
   ```

5. **Create `packages.txt`** for system dependencies:
   ```
   libgl1-mesa-glx
   libglib2.0-0
   ```

6. **Your Space is live!** 🎉

For detailed instructions, see [HUGGINGFACE_DEPLOYMENT.md](HUGGINGFACE_DEPLOYMENT.md)

</details>

### Docker Deployment

```bash
# Build Docker image
docker build -t image-ai-platform .

# Run container
docker run -p 8501:8501 image-ai-platform
```

---

## 💡 Usage Guide

### Single Image Processing

1. **Upload Image**
   - Drag & drop or click to upload
   - Supports: PNG, JPG, JPEG, BMP, TIFF
   - Or select from sample images

2. **Preprocess (Optional)**
   - Navigate to "Image & Preprocessing" tab
   - Choose preset: Auto Enhance, Custom, or None
   - View quality score and metrics

3. **Extract Text**
   - Go to "OCR & Text" tab
   - Select language(s)
   - Click "Extract Text"
   - Download results

4. **Generate Caption**
   - Switch to "AI Caption" tab
   - Select mode (Local/Cloud)
   - Click "Generate Caption"

5. **Translate**
   - Navigate to "Translation" tab
   - Choose target language
   - Download SRT or text

6. **Create Audio**
   - Go to "Text-to-Speech" tab
   - Select output language (auto-translates!)
   - Adjust speech rate
   - Download WAV file

### Batch Processing

<details>
<summary><b>Process multiple images efficiently</b></summary>

1. **Switch Mode**: Sidebar → Processing Mode → Batch Processing
2. **Upload Images**: Select multiple files
3. **Configure**: Choose OCR, Caption, Translation options
4. **Process**: Click "Process All Images"
5. **Download**: Get ZIP package with all results

</details>

---

## 📊 Technical Stack

<table>
<tr>
<td><b>Category</b></td>
<td><b>Technology</b></td>
<td><b>Purpose</b></td>
</tr>
<tr>
<td>Frontend</td>
<td>Streamlit</td>
<td>Web interface & UI components</td>
</tr>
<tr>
<td>OCR</td>
<td>EasyOCR</td>
<td>Multi-language text extraction</td>
</tr>
<tr>
<td>AI Model</td>
<td>BLIP (Salesforce)</td>
<td>Image captioning</td>
</tr>
<tr>
<td>Translation</td>
<td>Deep Translator</td>
<td>Google Translate API wrapper</td>
</tr>
<tr>
<td>TTS</td>
<td>pyttsx3 + macOS say</td>
<td>Text-to-speech synthesis</td>
</tr>
<tr>
<td>Image Processing</td>
<td>OpenCV + PIL</td>
<td>Preprocessing & enhancement</td>
</tr>
<tr>
<td>Deep Learning</td>
<td>PyTorch + Transformers</td>
<td>Model inference</td>
</tr>
<tr>
<td>Export</td>
<td>ReportLab + python-docx</td>
<td>PDF & DOCX generation</td>
</tr>
</table>

### Supported Languages

#### OCR (7 languages)
🇬🇧 English • 🇮🇳 Hindi • 🇮🇳 Kannada • 🇮🇳 Tamil • 🇮🇳 Telugu • 🇮🇳 Marathi • 🇮🇳 Bengali

#### Translation (19 languages)
🇬🇧 English • 🇮🇳 Hindi • 🇮🇳 Kannada • 🇮🇳 Tamil • 🇮🇳 Telugu • 🇮🇳 Marathi • 🇮🇳 Bengali • 🇮🇳 Gujarati • 🇮🇳 Malayalam • 🇪🇸 Spanish • 🇫🇷 French • 🇩🇪 German • 🇮🇹 Italian • 🇵🇹 Portuguese • 🇯🇵 Japanese • 🇰🇷 Korean • 🇨🇳 Chinese • 🇷🇺 Russian • 🇸🇦 Arabic

#### TTS (9 languages)
🇬🇧 English • 🇮🇳 Hindi • 🇮🇳 Kannada • 🇮🇳 Tamil • 🇮🇳 Telugu • 🇮🇳 Marathi • 🇮🇳 Bengali • 🇮🇳 Gujarati • 🇮🇳 Malayalam

---

## 📁 Project Structure

```
Image-AI-Platform/
├── src/                          # Source code
│   ├── app_pro.py               # Professional edition (full features)
│   ├── app_enhanced.py          # Standard edition
│   ├── app.py                   # Basic version
│   ├── ocr_engine.py            # OCR functionality
│   ├── caption_engine.py        # AI captioning
│   ├── translation_engine.py   # Translation engine
│   ├── tts_engine.py            # Text-to-speech
│   ├── image_processor.py       # Advanced preprocessing
│   └── export_engine.py         # Multi-format export
│
├── sample_images/               # Test images
│   ├── *.jpg                    # Sample files
│   └── README.md
│
├── requirements.txt             # Python dependencies
├── run.sh                       # Standard launcher
├── run_pro.sh                   # Professional launcher
├── demo.py                      # Demo & verification script
├── README.md                    # This file
├── README_PRO.md                # Professional edition guide
├── FEATURE_SHOWCASE.md          # Detailed features
├── SAMPLE_IMAGES_GUIDE.md       # Sample usage guide
├── TESTING_GUIDE.md             # Testing documentation
└── LICENSE                      # MIT License
```

---

## 🎯 Use Cases

<table>
<tr>
<td width="50%">

### 🎓 Education
- Digitize textbooks and notes
- Create multilingual study materials
- Generate audio lessons
- Extract text from lecture slides
- Translate educational content

### ♿ Accessibility
- Convert images to speech for visually impaired
- Translate documents for language learners
- Create audio books from images
- Assist with document reading

</td>
<td width="50%">

### 💼 Business
- Digitize receipts and invoices
- Extract data from forms
- Translate product descriptions
- Create marketing content
- Automate document processing

### 🔬 Research
- Analyze historical documents
- Process survey images
- Extract data from charts
- Multi-language research
- Archive digitization

</td>
</tr>
</table>

---

## 📈 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| OCR (single image) | 2-5s | Depends on image complexity |
| AI Caption (local) | 5-10s | First run downloads model (~1GB) |
| AI Caption (cloud) | 1-3s | Requires internet |
| Translation | <1s | Very fast |
| TTS Generation | 1-3s | Per 100 words |
| Batch (10 images) | 60-90s | Full processing |
| Quality Assessment | 0.5s | Real-time |
| Export (PDF/DOCX) | 1-2s | Per document |

---

## 🆚 Editions Comparison

| Feature | Standard | Professional |
|---------|----------|--------------|
| Multi-Language OCR | ✅ | ✅ |
| AI Image Captioning | ✅ | ✅ |
| Translation (19 languages) | ✅ | ✅ |
| Smart TTS | ✅ | ✅ |
| Basic Export (TXT) | ✅ | ✅ |
| **Image Preprocessing** | ❌ | ✅ |
| **Quality Assessment** | ❌ | ✅ |
| **Batch Processing** | ❌ | ✅ |
| **Multi-Format Export** | ❌ | ✅ (PDF, DOCX, JSON, SRT) |
| **ZIP Packages** | ❌ | ✅ |
| **Processing History** | ❌ | ✅ |
| **Analytics Dashboard** | ❌ | ✅ |
| **Professional UI Theme** | ❌ | ✅ |

---

## 🛠️ Configuration

### Environment Variables (Optional)

```bash
# Hugging Face API Token (for cloud captioning)
export HUGGINGFACE_TOKEN="your_token_here"

# Processing Options
export MAX_BATCH_SIZE=50
export ENABLE_GPU=true
export CACHE_DIR="./cache"
```

### Custom Settings

Edit `src/app_pro.py` to customize:
- Default languages
- Speech rates
- Processing presets
- UI themes
- Export formats

---

## 🐛 Troubleshooting

<details>
<summary><b>Common Issues & Solutions</b></summary>

### Installation Issues

**Problem**: `Module not found` errors
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**Problem**: CUDA/GPU errors
```bash
# Solution: Install CPU-only PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Runtime Issues

**Problem**: TTS not working
- Verify system has speech synthesis installed
- Check language-voice compatibility
- Try different voice/language combination

**Problem**: Slow performance
- Use Cloud API mode for captioning
- Disable quality assessment
- Process smaller batches
- Reduce image preprocessing

**Problem**: Export failures
- Ensure reportlab and python-docx are installed
- Check write permissions
- Try different export format

### Deployment Issues

**Problem**: Hugging Face Space timeout
- Use CPU-optimized models
- Reduce batch size
- Enable caching
- Use lighter preprocessing

</details>

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs**: Open an issue with details
- 💡 **Suggest Features**: Share your ideas
- 📝 **Improve Docs**: Fix typos, add examples
- 🔧 **Submit PRs**: Add features or fix bugs
- ⭐ **Star the Repo**: Show your support!

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/Image-AI-Platform.git
cd Image-AI-Platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -r requirements.txt
pip install -e .

# Run tests
python -m pytest tests/

# Make changes and submit PR
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What this means:
✅ Commercial use  
✅ Modification  
✅ Distribution  
✅ Private use  

---

## 🙏 Acknowledgments

This project wouldn't be possible without these amazing open-source projects:

- **[EasyOCR](https://github.com/JaidedAI/EasyOCR)** - Multi-language OCR engine
- **[Salesforce BLIP](https://github.com/salesforce/BLIP)** - Image captioning model
- **[Hugging Face](https://huggingface.co/)** - Model hosting and transformers
- **[Deep Translator](https://github.com/nidhaloff/deep-translator)** - Translation API
- **[Streamlit](https://streamlit.io/)** - Web framework
- **[OpenCV](https://opencv.org/)** - Image processing
- **[PyTorch](https://pytorch.org/)** - Deep learning framework

Special thanks to:
- **Mohammed Saqhib** - [Original Image Caption AI](https://github.com/Mohammed-Saqhib/Image-Caption-Ai) inspiration
- All contributors and users of this project

---

## 📞 Support & Contact

### Get Help

- 📖 **Documentation**: Check our comprehensive guides
- 💬 **Discussions**: Join [GitHub Discussions](https://github.com/YOUR_USERNAME/Image-AI-Platform/discussions)
- 🐛 **Issues**: Report bugs on [GitHub Issues](https://github.com/YOUR_USERNAME/Image-AI-Platform/issues)
- 📧 **Email**: your.email@example.com

### Stay Updated

- ⭐ Star this repository
- 👀 Watch for updates
- 🍴 Fork to contribute
- 📢 Share with others

---

## 🎉 Project Stats

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/Image-AI-Platform?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/Image-AI-Platform?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/YOUR_USERNAME/Image-AI-Platform?style=social)

### Made with ❤️ for the community

</div>

---

## 🚀 Roadmap

### Coming Soon

- [ ] 🌐 REST API for developers
- [ ] 📱 Mobile app (React Native)
- [ ] 🎨 Custom model training interface
- [ ] 📊 Advanced analytics with charts
- [ ] 🔍 Object detection integration
- [ ] 💾 Cloud storage integration
- [ ] 🎯 Named entity recognition
- [ ] 🌈 Word cloud generation
- [ ] 🔐 User authentication
- [ ] 📈 Performance dashboard

### Future Enhancements

- GPU acceleration
- Real-time collaboration
- Custom voice cloning
- More AI models (GPT-4 Vision)
- Multilingual UI
- Browser extension
- API rate limiting
- Webhook integrations

---

## 📚 Documentation

- **[README_PRO.md](README_PRO.md)** - Professional Edition Guide
- **[FEATURE_SHOWCASE.md](FEATURE_SHOWCASE.md)** - Detailed Feature List
- **[SAMPLE_IMAGES_GUIDE.md](SAMPLE_IMAGES_GUIDE.md)** - Using Sample Images
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing & Verification
- **[HUGGINGFACE_DEPLOYMENT.md](HUGGINGFACE_DEPLOYMENT.md)** - Deployment Guide

---

<div align="center">

## ⭐ If you find this project useful, please give it a star!

### 🎯 Perfect for Final Year Projects, Research, and Production Use

**Built with passion and professional excellence**

[🚀 Get Started](#-quick-start) • [📖 Documentation](#-documentation) • [🤝 Contribute](#-contributing) • [💬 Discuss](https://github.com/YOUR_USERNAME/Image-AI-Platform/discussions)

---

**Version**: 2.0 Professional Edition  
**Last Updated**: November 2024  
**Status**: Production Ready ✅

</div>
