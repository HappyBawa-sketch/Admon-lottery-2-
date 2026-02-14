# LINE Sticker Pack Generator

This directory contains a script and generated assets for a LINE sticker pack based on `source_image.jpg`.

## Contents

- `generate_stickers.py`: The Python script used to generate the stickers.
- `stickers/`: The directory containing the generated PNG images.
    - `01.png` to `36.png`: The sticker images (370x320 px).
    - `main.png`: The main image for the LINE store (240x240 px).
    - `tab.png`: The tab image for the chat room (96x74 px).
- `source_image.jpg`: The original source image used.

## How to Modify

If you want to change the text phrases or the source image:

1.  Replace `source_image.jpg` with your desired image.
2.  Edit `generate_stickers.py` to change the `PHRASES` list or adjust fonts/colors.
3.  Run the script:

```bash
python3 generate_stickers.py
```

## Requirements

- Python 3
- Pillow (`pip install Pillow`)
