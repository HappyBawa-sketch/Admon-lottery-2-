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

def create_frame(base_img, scale, canvas_size, text, font):
    """
    Creates a single frame with the image scaled by `scale` factor.
    """
    W, H = canvas_size

    # Create canvas
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))

    # Calculate new size for the image
    if base_img:
        w, h = base_img.size
        new_w = int(w * scale)
        new_h = int(h * scale)

        # Resize using LANCZOS
        resized = base_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # Center position
        x = (W - new_w) // 2
        y = (H - new_h) // 2

        canvas.paste(resized, (x, y))

    # Draw text (static position or could be scaled too, let's keep it static relative to canvas corners
    # OR move it slightly? Let's keep it static for readability while image pulses,
    # OR pulse the text too. Pulsing the whole canvas is easier but background is transparent.
    # Let's draw text on the canvas.

    if text:
        draw = ImageDraw.Draw(canvas)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # Position: Bottom Right
        text_x = W - text_w - 10
        text_y = H - text_h - 10

        # Clamp
        text_x = max(0, text_x)
        text_y = max(0, text_y)

        # Outline
        outline_color = "white"
        text_color = "black"
        thickness = 3

        for dx in range(-thickness, thickness+1):
            for dy in range(-thickness, thickness+1):
                if dx == 0 and dy == 0: continue
                draw.text((text_x + dx, text_y + dy), text, font=font, fill=outline_color)

        draw.text((text_x, text_y), text, font=font, fill=text_color)

    return canvas

# Process
try:
    img = Image.open(source_path)

    # Crop (0, 80, 1080, 2320)
    crop_box = (0, 80, 1080, 2320)
    img_cropped = img.crop(crop_box)

    # Target size for LINE Animation: 320x270
    MAX_W, MAX_H = 320, 270

    # Prepare base resized image (fitting in box with some padding for animation)
    # We leave 10% padding so scaling up 1.1x doesn't clip
    PADDING_FACTOR = 0.9
    TARGET_W = int(MAX_W * PADDING_FACTOR)
    TARGET_H = int(MAX_H * PADDING_FACTOR)

    img_ratio = img_cropped.width / img_cropped.height
    target_ratio = TARGET_W / TARGET_H

    if img_ratio > target_ratio:
        base_w = TARGET_W
        base_h = int(TARGET_W / img_ratio)
    else:
        base_h = TARGET_H
        base_w = int(TARGET_H * img_ratio)

    img_base = img_cropped.resize((base_w, base_h), Image.Resampling.LANCZOS)

    # Font
    try:
        if font_path:
            # Adjust font size for smaller image
            font = ImageFont.truetype(font_path, 32)
        else:
            raise IOError("No font found")
    except:
        print("Font not found, using default")
        font = ImageFont.load_default()

    # Animation scales (Pulse)
    scales = [1.0, 1.05, 1.1, 1.05]
    duration = 200 # ms per frame

    for i, text in enumerate(texts):
        frames = []
        for s in scales:
            frame = create_frame(img_base, s, (MAX_W, MAX_H), text, font)
            frames.append(frame)

        # Save as APNG
        filename = f"{i+1:02d}.png"
        save_path = os.path.join(output_dir, filename)

        # Save
        frames[0].save(
            save_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            disposal=2 # Clear background before next frame
        )
        print(f"Saved animated {save_path}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
