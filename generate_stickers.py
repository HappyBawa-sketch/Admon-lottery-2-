import os
from PIL import Image, ImageDraw, ImageFont

# Configuration
SOURCE_IMAGE = "source_image.jpg"
OUTPUT_DIR = "stickers"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TEXT_COLOR = (0, 0, 0) # Black
OUTLINE_COLOR = (255, 255, 255) # White
OUTLINE_WIDTH = 3

# LINE Sticker Dimensions (W x H)
STICKER_SIZE = (370, 320)
MAIN_SIZE = (240, 240)
TAB_SIZE = (96, 74)

# 36 Phrases
PHRASES = [
    "Hi", "Hello", "Good Morning", "Good Night",
    "Bye", "See you", "Thanks", "Thank you",
    "Sorry", "Excuse me", "OK", "Yes",
    "No", "Good", "Bad", "LOL",
    "Haha", "Love", "Like", "Wow",
    "What?", "Really?", "Please", "Help",
    "Busy", "Tired", "Hungry", "Angry",
    "Sad", "Happy", "Congrats", "Good Luck",
    "Nice", "Cool", "OMG", "..."
]

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_and_resize_image(filepath, target_size):
    """
    Resizes image to fit within target_size while maintaining aspect ratio.
    Returns a new RGBA image of size target_size with the resized image centered.
    """
    img = Image.open(filepath).convert("RGBA")

    # Calculate resize ratio
    width_ratio = target_size[0] / img.width
    height_ratio = target_size[1] / img.height
    scale = min(width_ratio, height_ratio)

    new_width = int(img.width * scale)
    new_height = int(img.height * scale)

    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create transparent canvas
    canvas = Image.new("RGBA", target_size, (255, 255, 255, 0))

    # Center position
    x = (target_size[0] - new_width) // 2
    y = (target_size[1] - new_height) // 2

    canvas.paste(resized_img, (x, y))
    return canvas

def draw_text_with_outline(draw, text, font, canvas_size):
    """
    Draws text centered at the bottom of the image with an outline.
    """
    # Calculate text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Position: Centered horizontally, 20px from bottom
    x = (canvas_size[0] - text_width) // 2
    y = canvas_size[1] - text_height - 20

    # Draw outline
    for adj_x in range(-OUTLINE_WIDTH, OUTLINE_WIDTH + 1):
        for adj_y in range(-OUTLINE_WIDTH, OUTLINE_WIDTH + 1):
            draw.text((x + adj_x, y + adj_y), text, font=font, fill=OUTLINE_COLOR)

    # Draw text
    draw.text((x, y), text, font=font, fill=TEXT_COLOR)

def generate_stickers():
    ensure_dir(OUTPUT_DIR)

    # Load font - adjust size based on typical sticker size
    font_size = 40
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except IOError:
        print(f"Font not found at {FONT_PATH}. Using default.")
        font = ImageFont.load_default()

    # Generate 36 stickers
    for i, phrase in enumerate(PHRASES):
        idx = i + 1
        filename = f"{idx:02d}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # Create base sticker
        sticker = load_and_resize_image(SOURCE_IMAGE, STICKER_SIZE)
        draw = ImageDraw.Draw(sticker)

        # Add text
        draw_text_with_outline(draw, phrase, font, STICKER_SIZE)

        sticker.save(filepath, "PNG")
        print(f"Generated {filepath}")

    # Generate Main Image (used for display in store) - Use the first phrase or image
    main_img = load_and_resize_image(SOURCE_IMAGE, MAIN_SIZE)
    # Optional: Add text to main image too, or keep clean.
    # Usually main image represents the pack. Let's add the first phrase "Hi"
    draw_main = ImageDraw.Draw(main_img)
    font_main = ImageFont.truetype(FONT_PATH, 30) # Smaller font
    draw_text_with_outline(draw_main, "Hi", font_main, MAIN_SIZE)
    main_img.save(os.path.join(OUTPUT_DIR, "main.png"), "PNG")
    print(f"Generated main.png")

    # Generate Tab Image (icon in chat)
    tab_img = load_and_resize_image(SOURCE_IMAGE, TAB_SIZE)
    tab_img.save(os.path.join(OUTPUT_DIR, "tab.png"), "PNG")
    print(f"Generated tab.png")

if __name__ == "__main__":
    generate_stickers()
