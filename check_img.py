
from PIL import Image
import os

files = [
    r"d:\project\rainieeblog\src\assets\hero-ai-tool-evaluation.jpg",
    r"d:\project\rainieeblog\src\assets\blog-placeholder-1.jpg",
    r"d:\project\rainieeblog\src\assets\hero-clawdbot.jpg"
]

for f in files:
    try:
        if os.path.exists(f):
            with Image.open(f) as img:
                size_kb = os.path.getsize(f) / 1024
                print(f"File: {os.path.basename(f)} | Size: {size_kb:.2f} KB | Dimensions: {img.width}x{img.height} | Format: {img.format} | Mode: {img.mode}")
        else:
            print(f"File not found: {f}")
    except Exception as e:
        print(f"Error reading {f}: {e}")
