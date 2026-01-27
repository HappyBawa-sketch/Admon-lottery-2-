from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
source_path = '/tmp/file_attachments/Screenshot_2026-01-27-18-16-18-11_94c3c0214f41e8559bec03caf75c21c7.jpg'
output_dir = 'stickers'
# Try to find a bold font
font_candidates = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf',
    'arialbd.ttf',
    'Arial Bold.ttf'
]

font_path = None
for path in font_candidates:
    if os.path.exists(path):
        font_path = path
        break

os.makedirs(output_dir, exist_ok=True)

# Texts
texts = [
    "Hello", "Hi!", "Good Morning", "Good Night", "Thanks", "Thank You",
    "Sorry", "Excuse me", "OK", "Okay", "Yes", "No",
    "Please", "Bye", "See you", "Good luck", "Congrats", "Happy",
    "Sad", "Angry", "Love", "Like", "Good Job", "Wow",
    "LOL", "OMG", "Really?", "What?", "Busy", "Free?",
    "Call me", "On my way", "Late", "Done", "Cheers", "..."
]

# Ensure we have exactly 36
if len(texts) < 36:
    texts.extend([""] * (36 - len(texts)))
texts = texts[:36]

# Process
try:
    img = Image.open(source_path)

    # Crop (0, 80, 1080, 2320)
    crop_box = (0, 80, 1080, 2320)
    img_cropped = img.crop(crop_box)

    # Target size
    MAX_W, MAX_H = 370, 320

    # Resize to fit within MAX_W x MAX_H preserving aspect ratio
    img_ratio = img_cropped.width / img_cropped.height
    target_ratio = MAX_W / MAX_H

    if img_ratio > target_ratio:
        # Width limited
        new_w = MAX_W
        new_h = int(MAX_W / img_ratio)
    else:
        # Height limited
        new_h = MAX_H
        new_w = int(MAX_H * img_ratio)

    img_resized = img_cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Font
    try:
        if font_path:
            font = ImageFont.truetype(font_path, 40)
        else:
            raise IOError("No font found")
    except:
        print("Font not found, using default")
        font = ImageFont.load_default()

    for i, text in enumerate(texts):
        # Create canvas
        canvas = Image.new('RGBA', (MAX_W, MAX_H), (0, 0, 0, 0))

        # Paste image in center
        paste_x = (MAX_W - new_w) // 2
        paste_y = (MAX_H - new_h) // 2

        # Paste (ensure RGB mode for paste if source is JPG)
        canvas.paste(img_resized, (paste_x, paste_y))

        # Add text
        draw = ImageDraw.Draw(canvas)

        # Calculate text size using textbbox
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # Position text: Bottom Right with some padding
        # If text is empty, skip
        if text:
            text_x = MAX_W - text_w - 20
            text_y = MAX_H - text_h - 20

            # Ensure text stays within bounds (simple clamp)
            text_x = max(0, text_x)
            text_y = max(0, text_y)

            # Outline
            outline_color = "white"
            text_color = "black"
            thickness = 3

            # Draw outline
            for dx in range(-thickness, thickness+1):
                for dy in range(-thickness, thickness+1):
                    if dx == 0 and dy == 0: continue
                    draw.text((text_x + dx, text_y + dy), text, font=font, fill=outline_color)

            # Draw text
            draw.text((text_x, text_y), text, font=font, fill=text_color)

        # Save
        filename = f"{i+1:02d}.png"
        save_path = os.path.join(output_dir, filename)
        canvas.save(save_path, "PNG")
        print(f"Saved {save_path}")

except Exception as e:
    print(f"Error: {e}")
