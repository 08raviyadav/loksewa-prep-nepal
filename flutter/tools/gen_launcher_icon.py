#!/usr/bin/env python3
"""Generate the LokSewa Vidyapeeth Android launcher icons + splash art.

Why this script exists: the repo is pushed via a snapshot flow that rejects
binary files, so the launcher PNGs (mipmap-*, drawable-*) and the
gradle-wrapper.jar cannot be committed. CI regenerates the PNGs with this
script before `flutter build apk` — see
.github/workflows/flutter-release.yml.

The icon is the orange Devanagari "lo" on white (#FFFFFF), drawn with
Noto Sans Devanagari Bold — the same design as the original
assets/icon/app_icon.png (1024x1024), which is NOT in the repo (binary).
Glyph placement was measured from that original: the ink spans 20%-80%
of the width and its vertical centre sits at 47% of the height.

Outputs (all RGB PNGs, LANCZOS-downscaled from one 1024px master):
  android/app/src/main/res/mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/
      ic_launcher.png                       48/72/96/144/192 px
  android/app/src/main/res/drawable-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/
      ic_launcher_foreground.png            108/162/216/324/432 px
      splash.png                            256/384/512/768/1024 px
  android/app/src/main/res/drawable/background.png          1x1 white
  android/app/src/main/res/drawable-v21/background.png      1x1 white

Font: Noto Sans Devanagari Bold. Discovery order:
  1. --font PATH (or $LOKSEWA_ICON_FONT)
  2. well-known system paths (/usr/share/fonts/... on Ubuntu/Debian)
  3. `fc-list` lookup for "Noto Sans Devanagari" bold
  If no font is found the script FAILS with install instructions — it never
  silently renders with a fallback font, because a non-Devanagari font would
  draw tofu boxes instead of "lo". On Ubuntu/Debian:
      sudo apt-get install -y fonts-noto-core
  (fonts-noto-core ships NotoSansDevanagari-Bold.ttf; verified against the
  Debian package file list.)

Requires: Python 3.8+ and Pillow (`pip install pillow`).
Usage:
  python3 flutter/tools/gen_launcher_icon.py [--project-root PATH]
                                             [--font PATH]
                                             [--store-icon PATH]
  --store-icon saves an extra 1024x1024 master copy (for the Play Store
  listing, which wants a 512x512 icon — downscale this file).

Run from anywhere; --project-root defaults to the Flutter project root
(the parent of this script's directory).
"""

import argparse
import glob
import os
import subprocess
import sys

# Orange "lo" on white — the app's brand colours (also in pubspec.yaml's
# flutter_launcher_icons / flutter_native_splash config).
WHITE = (255, 255, 255)  # #FFFFFF
ORANGE = (234, 88, 12)  # #EA580C
GLYPH = "\u0932\u094b"  # Devanagari "lo"

MASTER_SIZE = 1024
# Ink geometry measured from the original app_icon.png (1024x1024):
# glyph ink spans x 206-818 (width 612) and its vertical centre is y 481.
GLYPH_WIDTH = 612
GLYPH_CENTER_Y = 481

DENSITIES = ("mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi")
MIPMAP_SIZES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144,
                "xxxhdpi": 192}
FOREGROUND_SIZES = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324,
                    "xxxhdpi": 432}
SPLASH_SIZES = {"mdpi": 256, "hdpi": 384, "xhdpi": 512, "xxhdpi": 768,
                "xxxhdpi": 1024}

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-Bold.ttf",
    "/usr/share/fonts/noto/NotoSansDevanagari-Bold.ttf",
    "/usr/local/share/fonts/NotoSansDevanagari-Bold.ttf",
    os.path.expanduser("~/.fonts/NotoSansDevanagari-Bold.ttf"),
    os.path.expanduser("~/.local/share/fonts/NotoSansDevanagari-Bold.ttf"),
]
FONT_GLOBS = [
    "/usr/share/fonts/**/NotoSansDevanagari-Bold.ttf",
    "/usr/local/share/fonts/**/NotoSansDevanagari-Bold.ttf",
]


def find_font(explicit):
    """Return a path to Noto Sans Devanagari Bold, or None."""
    if explicit:
        if os.path.isfile(explicit):
            return explicit
        print(f"error: --font path does not exist: {explicit}", file=sys.stderr)
        return None
    env_font = os.environ.get("LOKSEWA_ICON_FONT")
    if env_font:
        if os.path.isfile(env_font):
            return env_font
        print(f"error: LOKSEWA_ICON_FONT does not exist: {env_font}",
              file=sys.stderr)
        return None
    for path in FONT_CANDIDATES:
        if os.path.isfile(path):
            return path
    for pattern in FONT_GLOBS:
        matches = sorted(glob.glob(pattern, recursive=True))
        if matches:
            return matches[0]
    # Last resort: ask fontconfig.
    try:
        out = subprocess.run(
            ["fc-list", "Noto Sans Devanagari:bold", "file"],
            capture_output=True, text=True, timeout=30,
        )
        for line in out.stdout.splitlines():
            path = line.strip().split(":")[0]
            if path.endswith(".ttf") and os.path.isfile(path):
                return path
    except (FileNotFoundError, subprocess.SubprocessError):
        pass
    return None


def render_master(font_path):
    """Render the 1024x1024 master icon. Returns a PIL RGB image."""
    from PIL import Image, ImageDraw, ImageFont

    # Render the glyph huge on a transparent layer, then scale by its INK
    # bounding box (not font metrics — Devanagari ink sits high in the em
    # box, so anchor-based centring would misplace it).
    font = ImageFont.truetype(font_path, 1000)
    layer = Image.new("RGBA", (1600, 1600), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.text((800, 800), GLYPH, font=font, fill=ORANGE + (255,),
              anchor="mm")
    bbox = layer.getbbox()
    if bbox is None:
        raise RuntimeError("font rendered no glyphs — is this a "
                           "Devanagari-capable font?")
    glyph = layer.crop(bbox)
    scale = GLYPH_WIDTH / glyph.size[0]
    new_size = (GLYPH_WIDTH, round(glyph.size[1] * scale))
    glyph = glyph.resize(new_size, Image.LANCZOS)

    master = Image.new("RGB", (MASTER_SIZE, MASTER_SIZE), WHITE)
    x = (MASTER_SIZE - new_size[0]) // 2
    y = GLYPH_CENTER_Y - new_size[1] // 2
    master.paste(glyph, (x, y), glyph)
    return master


def main():
    parser = argparse.ArgumentParser(
        description="Generate Android launcher icons + splash art.")
    parser.add_argument("--project-root", default=None,
                        help="Flutter project root (default: auto-detect)")
    parser.add_argument("--font", default=None,
                        help="Path to NotoSansDevanagari-Bold.ttf")
    parser.add_argument("--store-icon", default=None, metavar="PATH",
                        help="Also save the 1024x1024 master to PATH "
                             "(for the Play Store listing)")
    args = parser.parse_args()

    if args.project_root:
        project_root = os.path.abspath(args.project_root)
    else:
        project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
    res_dir = os.path.join(project_root, "android", "app", "src", "main",
                           "res")
    if not os.path.isdir(res_dir):
        print(f"error: Android res dir not found: {res_dir}", file=sys.stderr)
        return 1

    try:
        from PIL import Image  # noqa: F401  (import check)
    except ImportError:
        print("error: Pillow is required: pip install pillow",
              file=sys.stderr)
        return 1

    font_path = find_font(args.font)
    if font_path is None:
        print("error: no Noto Sans Devanagari Bold font found.", file=sys.stderr)
        print("  Ubuntu/Debian:  sudo apt-get install -y fonts-noto-core",
              file=sys.stderr)
        print("  Or pass one explicitly:  --font /path/to/"
              "NotoSansDevanagari-Bold.ttf", file=sys.stderr)
        return 1
    print(f"Using font: {font_path}")

    master = render_master(font_path)
    outputs = []

    for density in DENSITIES:
        d = os.path.join(res_dir, f"mipmap-{density}")
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "ic_launcher.png")
        master.resize((MIPMAP_SIZES[density], MIPMAP_SIZES[density]),
                      Image.LANCZOS).save(p)
        outputs.append((p, MIPMAP_SIZES[density]))

    for density in DENSITIES:
        d = os.path.join(res_dir, f"drawable-{density}")
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "ic_launcher_foreground.png")
        master.resize((FOREGROUND_SIZES[density], FOREGROUND_SIZES[density]),
                      Image.LANCZOS).save(p)
        outputs.append((p, FOREGROUND_SIZES[density]))
        p = os.path.join(d, "splash.png")
        master.resize((SPLASH_SIZES[density], SPLASH_SIZES[density]),
                      Image.LANCZOS).save(p)
        outputs.append((p, SPLASH_SIZES[density]))

    for sub in ("drawable", "drawable-v21"):
        d = os.path.join(res_dir, sub)
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "background.png")
        Image.new("RGB", (1, 1), WHITE).save(p)
        outputs.append((p, 1))

    if args.store_icon:
        master.save(args.store_icon)
        outputs.append((args.store_icon, MASTER_SIZE))

    # Verify everything landed at the right size.
    from PIL import Image as _Image
    for path, size in outputs:
        with _Image.open(path) as im:
            if im.size != (size, size):
                print(f"error: {path} is {im.size}, expected "
                      f"({size}, {size})", file=sys.stderr)
                return 1
    print(f"Generated {len(outputs)} icon files in {res_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
