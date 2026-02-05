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

    failures = 0
    for f in files:
        path = os.path.join(output_dir, f)
        try:
            img = Image.open(path)
            if img.format != 'PNG':
                print(f"FAIL: {f} is not PNG")
                failures += 1

            # LINE Animated Max: 320x270
            if img.width > 320 or img.height > 270:
                print(f"FAIL: {f} dimensions {img.size} exceed limit 320x270")
                failures += 1

            # Check animation
            if not getattr(img, 'is_animated', False):
                print(f"FAIL: {f} is NOT animated")
                failures += 1
            else:
                if img.n_frames < 2:
                    print(f"FAIL: {f} has only {img.n_frames} frames")
                    failures += 1

        except Exception as e:
            print(f"FAIL: Could not open {f}: {e}")
            failures += 1

    if failures == 0:
        print("Verification complete. All stickers valid and animated.")
    else:
        print(f"Verification finished with {failures} failures.")

if __name__ == "__main__":
    verify_stickers()
