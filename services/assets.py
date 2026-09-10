"""
BhashaSetu Asset Management Service
Handles branded logos, emblems, and visual assets with base64 caching.
"""

import os
import base64

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
_B64_CACHE = {}


def get_asset_path(filename: str) -> str:
    """Return absolute path to an asset in assets/ directory."""
    return os.path.join(ASSETS_DIR, filename)


def get_logo_base64(variant: str = "dark_optimized") -> str:
    """
    Return base64-encoded string of the requested logo variant.
    Variants: 'dark_optimized', 'transparent', 'icon', 'original'
    """
    filename_map = {
        "dark_optimized": "logo_dark_optimized.png",
        "transparent": "logo_transparent.png",
        "icon": "logo_icon.png",
        "original": "logo_original.png"
    }
    target_file = filename_map.get(variant, "logo_dark_optimized.png")
    
    if target_file in _B64_CACHE:
        return _B64_CACHE[target_file]

    file_path = os.path.join(ASSETS_DIR, target_file)
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            _B64_CACHE[target_file] = encoded
            return encoded
    return ""
