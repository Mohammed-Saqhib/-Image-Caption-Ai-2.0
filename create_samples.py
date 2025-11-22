#!/usr/bin/env python3
"""Generate sample images for the Image AI Platform"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create sample_images folder if it doesn't exist
os.makedirs('sample_images', exist_ok=True)

def create_text_sample(filename, text, bg_color, text_color, size=(800, 600)):
    """Create a sample image with text"""
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a larger font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Save image
    img.save(os.path.join('sample_images', filename))
    print(f"✅ Created {filename}")

# Create sample images
create_text_sample(
    'sample_1_english.jpg',
    'Hello World\nWelcome to AI Platform',
    'white',
    'black'
)

create_text_sample(
    'sample_2_hindi.jpg',
    'नमस्ते\nस्वागत है',
    '#f0f8ff',
    '#000080'
)

create_text_sample(
    'sample_3_mixed.jpg',
    'English & हिंदी\nMixed Language Text',
    '#fff5ee',
    '#8b4513'
)

create_text_sample(
    'sample_4_document.jpg',
    'INVOICE\nAmount: $100\nDate: Nov 22, 2025',
    'white',
    'navy',
    (1000, 700)
)

create_text_sample(
    'sample_5_menu.jpg',
    'MENU\nCoffee - $3\nTea - $2\nCake - $5',
    '#fffacd',
    '#8b0000',
    (600, 800)
)

print("\n✨ All sample images created successfully!")
print("📁 Location: sample_images/")
