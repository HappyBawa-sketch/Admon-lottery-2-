import os
from PIL import Image

def verify_stickers():
    output_dir = 'stickers'
    if not os.path.exists(output_dir):
        print("FAIL: stickers directory missing")
        return

    files = sorted([f for f in os.listdir(output_dir) if f.endswith('.png')])

    if len(files) != 36:
        print(f"FAIL: Expected 36 files, found {len(files)}")
        return

    print(f"Found {len(files)} files.")

    for f in files:
        path = os.path.join(output_dir, f)
        try:
            img = Image.open(path)
            if img.format != 'PNG':
                print(f"FAIL: {f} is not PNG")
            if img.width > 370 or img.height > 320:
                print(f"FAIL: {f} dimensions {img.size} exceed limit")
            # print(f"OK: {f} {img.size}")
        except Exception as e:
            print(f"FAIL: Could not open {f}: {e}")

    print("Verification complete.")

if __name__ == "__main__":
    verify_stickers()
