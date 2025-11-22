# 📸 Sample Images Feature Guide

## ✨ New Feature Added!

Users can now choose between **uploading their own images** or **selecting from sample images** built into the application.

## 🎯 How It Works

### For Users:

1. **Open the app** at http://localhost:8501
2. You'll see two options:
   - **📤 Upload from Device** - Upload your own image files
   - **🖼️ Use Sample Image** - Select from pre-loaded samples

3. **Using Sample Images**:
   - Click the dropdown under "Use Sample Image"
   - Select any sample (e.g., `sample_1_english.jpg`)
   - See a preview of the selected image
   - The image will be automatically loaded for processing

### For Developers:

**Adding New Sample Images:**

1. Place images in the `sample_images/` folder
2. Supported formats: JPG, JPEG, PNG, BMP, WEBP
3. Naming convention: Use descriptive names (e.g., `sample_6_receipt.jpg`)
4. Images will automatically appear in the dropdown

**Sample Image Guidelines:**
- **Size**: 800x600 to 1920x1080 recommended
- **Content**: Should demonstrate different use cases (text, menus, mixed languages, documents)
- **Quality**: Clear, well-lit images work best for OCR

## 📋 Included Sample Images

1. **sample_1_english.jpg** - Simple English text
   - Use case: Basic OCR test
   - Features: Clear text, good contrast

2. **sample_2_hindi.jpg** - Hindi text
   - Use case: Multi-language OCR
   - Features: Devanagari script

3. **sample_3_mixed.jpg** - English & Hindi mixed
   - Use case: Multi-script detection
   - Features: Mixed language support

4. **sample_4_document.jpg** - Invoice/Document
   - Use case: Document processing
   - Features: Structured text

5. **sample_5_menu.jpg** - Menu card
   - Use case: Real-world application
   - Features: Pricing, formatting

## 🔧 Technical Implementation

### Code Changes:

**app_enhanced.py:**
- Added two-column layout for upload options
- Implemented sample image selection dropdown
- Added preview functionality for selected samples
- Handled both file uploads and file paths

**File Structure:**
```
Image Ai/
├── sample_images/
│   ├── README.md
│   ├── sample_1_english.jpg
│   ├── sample_2_hindi.jpg
│   ├── sample_3_mixed.jpg
│   ├── sample_4_document.jpg
│   └── sample_5_menu.jpg
└── create_samples.py (generator script)
```

### Creating More Samples:

Run the sample generator:
```bash
python3 create_samples.py
```

Or add your own images directly to the `sample_images/` folder.

## 💡 Benefits

✅ **Quick Testing** - No need to find test images
✅ **Demo Friendly** - Perfect for presentations
✅ **Feature Showcase** - Each sample demonstrates different capabilities
✅ **User Convenience** - Try before uploading personal images
✅ **Educational** - Shows what kinds of images work best

## 🎨 UI/UX Improvements

- **Side-by-side options** - Upload and sample selection in columns
- **Preview thumbnail** - See sample before selecting
- **Clear labels** - Intuitive interface
- **Seamless integration** - Works with all existing features (OCR, Caption, Translation, TTS)

---

**Status**: ✅ Feature Active
**Location**: http://localhost:8501
**Last Updated**: November 22, 2025
