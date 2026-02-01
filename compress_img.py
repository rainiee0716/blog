
from PIL import Image
import os

source = r"d:\project\rainieeblog\src\assets\hero-clawdbot.jpg"
target = r"d:\project\rainieeblog\src\assets\hero-clawdbot.jpg"

try:
    with Image.open(source) as img:
        # Save with lower quality
        img.save(target, quality=60, optimize=True)
        final_size = os.path.getsize(target) / 1024
        print(f"Reprocessed Size: {final_size:.2f} KB")

except Exception as e:
    print(f"Error: {e}")
