"""
🚀 AI Image Analysis Platform - FastAPI Backend
Professional REST API for OCR, AI Captioning, Translation & TTS
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import shutil
from pathlib import Path
import uuid
from datetime import datetime

# Import engines
from engines.ocr_engine import OCREngine
from engines.caption_engine import CaptionEngine
from engines.translation_engine import TranslationEngine
from engines.tts_engine import TTSEngine

# Initialize FastAPI app
app = FastAPI(
    title="AI Image Analysis API",
    description="Advanced OCR, AI Captioning, Translation & Text-to-Speech API",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize engines
print("🔧 Initializing AI engines...")
ocr_engine = OCREngine()
caption_engine = CaptionEngine()
translation_engine = TranslationEngine()
tts_engine = TTSEngine()
print("✅ All engines initialized!")

# Pydantic models
class TranslationRequest(BaseModel):
    text: str
    target_language: str

class TTSRequest(BaseModel):
    text: str
    language: str
    rate: Optional[int] = 200

class HealthResponse(BaseModel):
    status: str
    version: str
    engines: dict

# Helper functions
def save_upload_file(upload_file: UploadFile) -> Path:
    """Save uploaded file and return path"""
    file_id = str(uuid.uuid4())
    file_extension = Path(upload_file.filename).suffix
    file_path = UPLOAD_DIR / f"{file_id}{file_extension}"
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return file_path

def cleanup_file(file_path: Path):
    """Remove temporary file"""
    try:
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        print(f"Error cleaning up file: {e}")

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint"""
    return {
        "message": "🚀 AI Image Analysis API",
        "version": "2.0.0",
        "docs": "/api/docs",
        "endpoints": {
            "health": "/api/health",
            "ocr": "/api/ocr",
            "caption": "/api/caption",
            "translate": "/api/translate",
            "tts": "/api/tts"
        }
    }

@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "engines": {
            "ocr": "ready",
            "caption": "ready",
            "translation": "ready",
            "tts": "ready"
        }
    }

@app.post("/api/ocr", tags=["OCR"])
async def extract_text(
    file: UploadFile = File(...),
    languages: str = Form("en")
):
    """
    Extract text from image using OCR
    
    - **file**: Image file (JPG, PNG, etc.)
    - **languages**: Comma-separated language codes (e.g., 'en,hi,ar')
    """
    file_path = None
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file
        file_path = save_upload_file(file)
        
        # Parse languages
        lang_list = [lang.strip() for lang in languages.split(',')]
        
        # Extract text
        result = ocr_engine.extract_text(str(file_path), lang_list)
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "text": result["text"],
                "languages_detected": result.get("languages", lang_list),
                "confidence": result.get("confidence", 0.95),
                "word_count": len(result["text"].split()) if result["text"] else 0,
                "character_count": len(result["text"]) if result["text"] else 0
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if file_path:
            cleanup_file(file_path)

@app.post("/api/caption", tags=["AI Captioning"])
async def generate_caption(
    file: UploadFile = File(...),
    mode: str = Form("cloud"),
    detailed: bool = Form(True)
):
    """
    Generate AI caption for image using BLIP model with detailed description
    
    - **file**: Image file (JPG, PNG, etc.)
    - **mode**: 'local' or 'cloud' (default: cloud for faster processing)
    - **detailed**: Generate detailed description (default: True)
    """
    file_path = None
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file
        file_path = save_upload_file(file)
        
        # Generate caption with detailed description
        result = caption_engine.generate_caption(str(file_path), mode=mode, detailed=detailed)
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "caption": result["caption"],
                "detailed_description": result.get("detailed_description", result["caption"]),
                "mode": mode,
                "confidence": result.get("confidence", 0.90),
                "model": "Salesforce/blip-image-captioning-base",
                "has_detailed": detailed,
                "insights": result.get("insights", {})
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if file_path:
            cleanup_file(file_path)

@app.post("/api/translate", tags=["Translation"])
async def translate_text(request: TranslationRequest):
    """
    Translate text to target language
    
    - **text**: Text to translate
    - **target_language**: Target language code (en, hi, ar, es, fr, etc.)
    """
    try:
        result = translation_engine.translate(
            request.text,
            request.target_language
        )
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "original_text": request.text,
                "translated_text": result["translated_text"],
                "source_language": result.get("source_language", "auto"),
                "target_language": request.target_language,
                "word_count": len(result["translated_text"].split())
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tts", tags=["Text-to-Speech"])
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech
    
    - **text**: Text to convert to speech
    - **language**: Language code (en, hi, ar, etc.)
    - **rate**: Speech rate (50-400, default: 200)
    """
    try:
        result = tts_engine.generate_speech(
            request.text,
            request.language,
            request.rate
        )
        
        if result["success"]:
            audio_file = Path(result["audio_file"])
            
            # Determine media type based on file extension
            media_type = "audio/aiff" if audio_file.suffix == ".aiff" else "audio/wav"
            
            return FileResponse(
                path=str(audio_file),
                media_type=media_type,
                filename=f"speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}{audio_file.suffix}",
                headers={
                    "X-Character-Count": str(len(request.text)),
                    "X-Language": request.language
                }
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "TTS generation failed"))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/languages/ocr", tags=["Languages"])
async def get_ocr_languages():
    """Get supported OCR languages"""
    return {
        "languages": [
            {"code": "en", "name": "English"}
        ]
    }

@app.get("/api/languages/translation", tags=["Languages"])
async def get_translation_languages():
    """Get supported translation languages"""
    return {
        "languages": translation_engine.get_supported_languages()
    }

@app.get("/api/voices", tags=["Text-to-Speech"])
async def get_available_voices():
    """Get available TTS voices"""
    return {
        "voices": tts_engine.get_available_voices()
    }

# Run server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=7860,  # Hugging Face Spaces default port
        reload=True
    )
