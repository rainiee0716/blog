
from PIL import Image
import os

source = r"d:\project\rainieeblog\src\assets\hero-clawdbot.jpg"
target = r"d:\project\rainieeblog\src\assets\hero-clawdbot.jpg"

try:
    with Image.open(source) as img:
        print(f"Original: {img.width}x{img.height}")
        
        # Target Aspect Ratio 2:1 (Landscape)
        # We want to keep the width 1024, so height should be 512.
        # However, the image is 1024x1024.
        # We will crop the vertical center.
        
        target_width = 1024
        target_height = 512
        
        left = 0
        top = (img.height - target_height) / 2
        right = img.width
        bottom = (img.height + target_height) / 2
        
        img_cropped = img.crop((left, top, right, bottom))
        
        # Optional: Resize to 960x480 to match placeholder size strictly, or keep 1024x512.
        # Let's resize to 960x480 to be safe and smaller.
        img_final = img_cropped.resize((960, 480), Image.Resampling.LANCZOS)
        
        # Save with lower quality to match file size (~40KB)
        img_final.save(target, quality=75, optimize=True)
        
        final_size = os.path.getsize(target) / 1024
        print(f"Processed: {img_final.width}x{img_final.height}, Size: {final_size:.2f} KB")

except Exception as e:
    print(f"Error: {e}")
