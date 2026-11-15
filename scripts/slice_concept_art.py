#!/usr/bin/env python3
"""
Shinobi Sprint - Asset Preparation & Slicing Script
Extracts the 5 distinct horizontal depth layers for the night-time East Asian
forest theme from the provided reference concept art and exports optimized PNGs
for Flame's ParallaxComponent.

Layers produced:
1. Farthest Sky: Moon, nebula, stars, and distant mountain silhouettes (static depth)
2. Deep Background: Mountains, nighttime clouds, and pagoda spires
3. Mid Background: Misty bamboo forest, torii gate, and shrines
4. Midground Lamps: Traditional Japanese buildings and glowing warm orange lanterns
5. Foreground Path: River/stream with water reflections, rocks, and wooden path
"""

import argparse
import os
import sys
from PIL import Image, ImageFilter
import numpy as np


# Default coordinates within the reference concept art (1024x765)
DEFAULT_SLICES = {
    'farthest_sky': {
        'box': (528, 89, 1013, 209),
        'target_h': 512,
        'y_offset': 0,
        'fade_start': 0,
        'fade_end': 0,
        'description': 'Farthest Sky with static moon and glowing nebula',
    },
    'deep_background': {
        'box': (685, 210, 1013, 338),
        'target_h': 340,
        'y_offset': 172,
        'fade_start': 15,
        'fade_end': 110,
        'description': 'Deep Background with layered mountains and pagoda spires',
    },
    'mid_background': {
        'box': (685, 339, 1013, 468),
        'target_h': 310,
        'y_offset': 202,
        'fade_start': 25,
        'fade_end': 120,
        'description': 'Mid Background with misty bamboo forest and torii gate',
    },
    'midground_lamps': {
        'box': (685, 469, 1013, 600),
        'target_h': 260,
        'y_offset': 252,
        'fade_start': 15,
        'fade_end': 100,
        'description': 'Midground Lamps with traditional buildings and glowing lanterns',
    },
    'foreground_path': {
        'box': (685, 601, 1013, 749),
        'target_h': 190,
        'y_offset': 322,
        'fade_start': 10,
        'fade_end': 65,
        'description': 'Foreground Path with wooden walkway, rocks, and stream',
    },
}

CANVAS_WIDTH = 1024
CANVAS_HEIGHT = 512


def make_horizontal_seamless(pil_img: Image.Image, blend_width: int = 32) -> Image.Image:
    """
    Blends the left and right edges across blend_width pixels
    so the image tiles horizontally with zero visible seam.
    """
    arr = np.array(pil_img).astype(float)
    h, w, c = arr.shape
    actual_blend = min(blend_width, w // 4)
    for i in range(actual_blend):
        alpha = i / float(actual_blend)
        left_col = arr[:, i].copy()
        right_col = arr[:, w - actual_blend + i].copy()
        # Linear cross-fade
        blended = left_col * (1.0 - alpha) + right_col * alpha
        arr[:, w - actual_blend + i] = blended
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def process_layer(
    crop_img: Image.Image,
    target_h: int,
    y_offset: int,
    fade_start: int,
    fade_end: int,
    canvas_w: int = CANVAS_WIDTH,
    canvas_h: int = CANVAS_HEIGHT,
) -> Image.Image:
    """
    Scales a layer strip, applies seamless horizontal blending,
    creates smooth alpha transitions for depth layering, and pastes onto canvas.
    """
    seamless = make_horizontal_seamless(crop_img, blend_width=32)
    scaled = seamless.resize((canvas_w, target_h), Image.Resampling.LANCZOS)
    arr = np.array(scaled).astype(float)

    if fade_end > fade_start:
        alpha = np.zeros((target_h, canvas_w), dtype=float)
        for y in range(target_h):
            if y < fade_start:
                alpha[y, :] = 0.0
            elif y < fade_end:
                t = (y - fade_start) / float(fade_end - fade_start)
                # Smooth cosine curve for natural gradient
                smooth_t = 0.5 * (1.0 - np.cos(t * np.pi))
                alpha[y, :] = 255.0 * smooth_t
            else:
                alpha[y, :] = 255.0
        # Multiply with existing alpha if present
        if arr.shape[2] == 4:
            arr[:, :, 3] = np.minimum(arr[:, :, 3], alpha)
        else:
            arr = np.dstack([arr, alpha])
    elif arr.shape[2] == 3:
        # Full opacity
        alpha = np.full((target_h, canvas_w, 1), 255.0, dtype=float)
        arr = np.dstack([arr, alpha])

    canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    layer_patch = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    canvas.paste(layer_patch, (0, y_offset), layer_patch)
    return canvas


def slice_concept_art(
    image_path: str,
    output_dir: str,
    parallax_dir: str = None,
):
    """Slices concept art into 5 depth layers and saves them."""
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Concept art image not found: {image_path}")

    os.makedirs(output_dir, exist_ok=True)
    if parallax_dir:
        os.makedirs(parallax_dir, exist_ok=True)

    print(f"Loading concept art from: {image_path}")
    source = Image.open(image_path).convert('RGBA')
    print(f"Source image size: {source.size}")

    processed_layers = {}
    raw_crops = {}

    layer_keys = [
        'farthest_sky',
        'deep_background',
        'mid_background',
        'midground_lamps',
        'foreground_path',
    ]

    for key in layer_keys:
        cfg = DEFAULT_SLICES[key]
        box = cfg['box']
        crop = source.crop(box)
        raw_crops[key] = crop

        # Save raw slice strip
        raw_filename = f"raw_{key}.png"
        raw_path = os.path.join(output_dir, raw_filename)
        crop.save(raw_path, format='PNG', optimize=True)
        print(f"  Exported raw slice: {raw_filename} ({crop.size})")

        # Process into full canvas parallax layer
        layer_img = process_layer(
            crop_img=crop,
            target_h=cfg['target_h'],
            y_offset=cfg['y_offset'],
            fade_start=cfg['fade_start'],
            fade_end=cfg['fade_end'],
        )
        processed_layers[key] = layer_img

        # Save optimized PNG
        layer_filename = f"{key}.png"
        layer_path = os.path.join(output_dir, layer_filename)
        layer_img.save(layer_path, format='PNG', optimize=True)
        print(f"  Exported parallax layer: {layer_filename} ({layer_img.size}) - {cfg['description']}")

    # Also export composite preview for visual verification
    composite = processed_layers['farthest_sky'].copy()
    for key in ['deep_background', 'mid_background', 'midground_lamps', 'foreground_path']:
        composite.alpha_composite(processed_layers[key])

    preview_path = os.path.join(output_dir, 'parallax_preview_composite.png')
    composite.save(preview_path, format='PNG', optimize=True)
    print(f"  Exported composite preview: parallax_preview_composite.png")

    # If parallax_dir provided, sync compatibility filenames
    if parallax_dir:
        compat_mapping = {
            'farthest_sky': 'parallax_layer1_sky_moon.png',
            'deep_background': 'parallax_layer2_castle.png',
            'mid_background': 'parallax_layer3_trees_gates.png',
            'midground_lamps': 'parallax_layer4_lamps.png',
            'foreground_path': 'parallax_layer5_path.png',
        }
        for src_key, dst_name in compat_mapping.items():
            dst_path = os.path.join(parallax_dir, dst_name)
            processed_layers[src_key].save(dst_path, format='PNG', optimize=True)
            print(f"  Synced to parallax dir: {dst_name}")

    print("All 5 parallax layers successfully sliced and exported!")


def main():
    parser = argparse.ArgumentParser(description="Slice East Asian concept art into 5 parallax layers.")
    parser.add_argument(
        '--input',
        default=os.path.join('assets', 'concept_art.jpg'),
        help='Path to flat concept art image'
    )
    parser.add_argument(
        '--output',
        default=os.path.join('assets', 'images', 'backgrounds'),
        help='Destination directory for sliced layers'
    )
    parser.add_argument(
        '--parallax-output',
        default=os.path.join('assets', 'images', 'parallax'),
        help='Secondary destination directory for parallax assets compatibility'
    )
    args = parser.parse_args()

    slice_concept_art(
        image_path=args.input,
        output_dir=args.output,
        parallax_dir=args.parallax_output,
    )


if __name__ == '__main__':
    main()
