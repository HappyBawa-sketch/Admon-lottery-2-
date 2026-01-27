from PIL import Image

filepath = '/tmp/file_attachments/Screenshot_2026-01-27-18-16-18-11_94c3c0214f41e8559bec03caf75c21c7.jpg'

try:
    img = Image.open(filepath)
    width, height = img.size
    mid_x = width // 2

    threshold = 15

    top_bound = 0
    bottom_bound = height - 1

    # Scan from top down
    for y in range(height):
        pixel = img.getpixel((mid_x, y))
        if max(pixel) > threshold:
            top_bound = y
            break

    # Scan from bottom up
    for y in range(height - 1, -1, -1):
        pixel = img.getpixel((mid_x, y))
        if max(pixel) > threshold:
            bottom_bound = y
            break

    print(f"Vertical Content: {top_bound} to {bottom_bound}")
    print(f"Height of content: {bottom_bound - top_bound}")

    # Also check horizontal at the center of the DETECTED content
    content_mid_y = (top_bound + bottom_bound) // 2
    left_bound = 0
    right_bound = width - 1

    for x in range(width):
        pixel = img.getpixel((x, content_mid_y))
        if max(pixel) > threshold:
            left_bound = x
            break

    for x in range(width - 1, -1, -1):
        pixel = img.getpixel((x, content_mid_y))
        if max(pixel) > threshold:
            right_bound = x
            break

    print(f"Horizontal Content (at y={content_mid_y}): {left_bound} to {right_bound}")
    print(f"Width of content: {right_bound - left_bound}")

except Exception as e:
    print(f"Error: {e}")
