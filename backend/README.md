---
title: AI Image Analysis Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
license: mit
---

# 🚀 AI Image Analysis Platform - REST API

Professional REST API for OCR, AI Captioning, Translation & Text-to-Speech.

## Features

- 📸 **Multi-Language OCR** - Extract text in 19+ languages
- 🎨 **AI Image Captioning** - BLIP model for image descriptions  
- 🌍 **Translation** - Translate to 19+ languages
- 🎧 **Text-to-Speech** - Natural voice synthesis

## API Endpoints

- `POST /api/ocr` - Extract text from images
- `POST /api/caption` - Generate AI captions
- `POST /api/translate` - Translate text
- `POST /api/tts` - Text-to-speech conversion

## Documentation

Visit `/api/docs` for interactive API documentation.

## Usage

```python
import requests

# OCR Example
files = {'file': open('image.jpg', 'rb')}
data = {'languages': 'en,hi'}
response = requests.post('https://your-space.hf.space/api/ocr', files=files, data=data)
print(response.json())
```

Built with ❤️ by Mohammed Saqhib
