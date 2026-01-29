"""
Image utility functions
"""
import os
from PIL import Image
from typing import Optional, Tuple


def get_image_size(image_path: str) -> Optional[Tuple[int, int]]:
    """Get the size of an image file"""
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        print(f"Error getting image size: {e}")
        return None


def validate_image(image_path: str) -> bool:
    """Validate if file is a valid PNG image"""
    try:
        if not os.path.isfile(image_path):
            return False
        if not image_path.lower().endswith('.png'):
            return False
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception as e:
        print(f"Error validating image: {e}")
        return False


def resize_image_for_display(image_path: str, max_width: int = 1200, max_height: int = 800) -> Optional[Image.Image]:
    """Resize image to fit display while maintaining aspect ratio"""
    try:
        with Image.open(image_path) as img:
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            return img.copy()
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None
