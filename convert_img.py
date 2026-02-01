
from PIL import Image
import os

source = r"d:\project\rainieeblog\src\assets\hero_clawdbot.png"
target = r"d:\project\rainieeblog\src\assets\hero-clawdbot.jpg"

try:
    with Image.open(source) as img:
        # Resize if too huge (e.g. > 1200 width) to save space
        if img.width > 1200:
             ratio = 1200 / img.width
             new_height = int(img.height * ratio)
             img = img.resize((1200, new_height), Image.Resampling.LANCZOS)
        
        # Convert to RGB (in case of alpha channel in PNG) and save as JPG
        rgb_img = img.convert('RGB')
        rgb_img.save(target, quality=85)
        print(f"Successfully converted to {target}")
except Exception as e:
    print(f"Error: {e}")
