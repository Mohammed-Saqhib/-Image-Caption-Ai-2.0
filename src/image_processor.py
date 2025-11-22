"""
Advanced Image Processing Module
Provides preprocessing techniques to improve OCR accuracy
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io

class ImageProcessor:
    """Advanced image preprocessing for better OCR results"""
    
    def __init__(self):
        self.processing_history = []
    
    def pil_to_cv2(self, pil_image):
        """Convert PIL Image to OpenCV format"""
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    def cv2_to_pil(self, cv2_image):
        """Convert OpenCV image to PIL format"""
        return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))
    
    def denoise(self, image, strength=10):
        """
        Remove noise from image using Non-local Means Denoising
        
        Args:
            image: PIL Image
            strength: Denoising strength (1-30, higher = more denoising)
        
        Returns:
            PIL Image with reduced noise
        """
        cv2_img = self.pil_to_cv2(image)
        denoised = cv2.fastNlMeansDenoisingColored(cv2_img, None, strength, strength, 7, 21)
        self.processing_history.append("Denoising")
        return self.cv2_to_pil(denoised)
    
    def sharpen(self, image, factor=2.0):
        """
        Sharpen image for better text clarity
        
        Args:
            image: PIL Image
            factor: Sharpening factor (0.0 - 5.0)
        
        Returns:
            PIL Image with enhanced sharpness
        """
        enhancer = ImageEnhance.Sharpness(image)
        sharpened = enhancer.enhance(factor)
        self.processing_history.append(f"Sharpening ({factor}x)")
        return sharpened
    
    def adaptive_threshold(self, image, block_size=11, c=2):
        """
        Apply adaptive thresholding for better text extraction
        
        Args:
            image: PIL Image
            block_size: Size of neighborhood area (odd number)
            c: Constant subtracted from mean
        
        Returns:
            PIL Image with adaptive thresholding applied
        """
        cv2_img = self.pil_to_cv2(image)
        gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        
        # Ensure block_size is odd
        if block_size % 2 == 0:
            block_size += 1
        
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, block_size, c
        )
        
        # Convert back to RGB
        rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
        self.processing_history.append("Adaptive Threshold")
        return Image.fromarray(rgb)
    
    def deskew(self, image):
        """
        Automatically detect and correct skew/rotation in scanned documents
        
        Args:
            image: PIL Image
        
        Returns:
            PIL Image with corrected rotation
        """
        cv2_img = self.pil_to_cv2(image)
        gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        
        # Detect skew angle using Hough Line Transform
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        coords = np.column_stack(np.where(thresh > 0))
        
        if len(coords) < 5:  # Not enough points for deskewing
            self.processing_history.append("Deskew (No rotation needed)")
            return image
        
        angle = cv2.minAreaRect(coords)[-1]
        
        # Normalize angle
        if angle < -45:
            angle = 90 + angle
        elif angle > 45:
            angle = angle - 90
        
        # Only deskew if angle is significant
        if abs(angle) < 0.5:
            self.processing_history.append("Deskew (No rotation needed)")
            return image
        
        # Rotate image
        (h, w) = cv2_img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(cv2_img, M, (w, h), 
                                 flags=cv2.INTER_CUBIC, 
                                 borderMode=cv2.BORDER_REPLICATE)
        
        self.processing_history.append(f"Deskew ({angle:.2f}°)")
        return self.cv2_to_pil(rotated)
    
    def edge_enhance(self, image):
        """
        Enhance edges for better text detection
        
        Args:
            image: PIL Image
        
        Returns:
            PIL Image with enhanced edges
        """
        enhanced = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        self.processing_history.append("Edge Enhancement")
        return enhanced
    
    def contrast_stretch(self, image):
        """
        Automatically adjust contrast for optimal text visibility
        
        Args:
            image: PIL Image
        
        Returns:
            PIL Image with stretched contrast
        """
        cv2_img = self.pil_to_cv2(image)
        
        # Convert to LAB color space
        lab = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels
        lab = cv2.merge([l, a, b])
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        self.processing_history.append("Contrast Stretch (CLAHE)")
        return self.cv2_to_pil(result)
    
    def remove_borders(self, image, border_size=10):
        """
        Remove borders/margins from scanned documents
        
        Args:
            image: PIL Image
            border_size: Size of border to remove (pixels)
        
        Returns:
            PIL Image with borders removed
        """
        width, height = image.size
        cropped = image.crop((
            border_size, 
            border_size, 
            width - border_size, 
            height - border_size
        ))
        self.processing_history.append(f"Border Removal ({border_size}px)")
        return cropped
    
    def upscale(self, image, scale_factor=2):
        """
        Upscale low-resolution images for better OCR
        
        Args:
            image: PIL Image
            scale_factor: Scaling factor (1-4)
        
        Returns:
            PIL Image upscaled
        """
        width, height = image.size
        new_size = (int(width * scale_factor), int(height * scale_factor))
        upscaled = image.resize(new_size, Image.LANCZOS)
        self.processing_history.append(f"Upscale ({scale_factor}x)")
        return upscaled
    
    def auto_enhance(self, image, aggressive=False):
        """
        Apply a combination of preprocessing techniques automatically
        
        Args:
            image: PIL Image
            aggressive: If True, apply more aggressive preprocessing
        
        Returns:
            PIL Image with auto-enhancements applied
        """
        self.processing_history = []
        
        # Start with denoising
        result = self.denoise(image, strength=15 if aggressive else 10)
        
        # Deskew if needed
        result = self.deskew(result)
        
        # Enhance contrast
        result = self.contrast_stretch(result)
        
        # Sharpen for text clarity
        result = self.sharpen(result, factor=2.5 if aggressive else 2.0)
        
        # Apply adaptive threshold for aggressive mode
        if aggressive:
            result = self.adaptive_threshold(result)
        
        return result
    
    def get_processing_summary(self):
        """Get summary of applied processing steps"""
        return " → ".join(self.processing_history) if self.processing_history else "No processing applied"
    
    def quality_assessment(self, image):
        """
        Assess image quality for OCR readiness
        
        Args:
            image: PIL Image
        
        Returns:
            dict with quality metrics
        """
        cv2_img = self.pil_to_cv2(image)
        gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        
        # Calculate sharpness (Laplacian variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Calculate brightness
        brightness = np.mean(gray)
        
        # Calculate contrast (standard deviation)
        contrast = np.std(gray)
        
        # Overall quality score (0-100)
        sharpness_score = min(100, (laplacian_var / 10) * 100)
        brightness_score = 100 - abs(brightness - 128) / 1.28
        contrast_score = min(100, (contrast / 64) * 100)
        
        overall_score = (sharpness_score + brightness_score + contrast_score) / 3
        
        return {
            "overall_score": round(overall_score, 2),
            "sharpness": round(sharpness_score, 2),
            "brightness": round(brightness_score, 2),
            "contrast": round(contrast_score, 2),
            "recommendation": self._get_recommendation(overall_score)
        }
    
    def _get_recommendation(self, score):
        """Get recommendation based on quality score"""
        if score >= 80:
            return "Excellent quality - ready for OCR"
        elif score >= 60:
            return "Good quality - may benefit from light preprocessing"
        elif score >= 40:
            return "Fair quality - apply auto-enhancement"
        else:
            return "Poor quality - apply aggressive preprocessing"
