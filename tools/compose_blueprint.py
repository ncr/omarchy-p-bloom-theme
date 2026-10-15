#!/usr/bin/env python3
"""Compose generated artwork with exact SVG branding and outlined typography.

python3 tools/compose_blueprint.py concepts/blueprint-studies/10-truth-lamp.layout.json

The generated source is immutable. Optional cleanup is a one-time migration for
old art containing generated text. New source art should have no text or logo.
Requires pycairo, Pillow, numpy, OpenCV (cleanup only), fontconfig and librsvg.
"""

import argparse
import copy
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

import cairo
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def element(parent, tag, **attrs):
    return ET.SubElement(parent, f"{{{NS}}}{tag}", {k.replace("_", "-"): str(v) for k, v in attrs.items()})


def outlined_text(ctx, group, text, x, y, size, spacing, opacity=1, right=False, max_width=None):
    """Store actual font contours; the finished SVG never needs a font lookup."""
    ctx.set_font_size(size)
    advances = [ctx.text_extents(ch).x_advance for ch in text]
    width = sum(advances) + spacing * max(0, len(text) - 1)
    if max_width is not None and width > max_width:
        raise ValueError(f"Text exceeds reserved width ({width:.1f} > {max_width}): {text}")
    if right:
        x -= width
    ctx.new_path()
    for ch, advance in zip(text, advances):
        ctx.move_to(x, y)
        ctx.text_path(ch)
        x += advance + spacing
    commands = []
    for typ, coords in ctx.copy_path():
        command = {cairo.PATH_MOVE_TO: "M", cairo.PATH_LINE_TO: "L", cairo.PATH_CURVE_TO: "C", cairo.PATH_CLOSE_PATH: "Z"}[typ]
        commands.append(command + " ".join(f"{v:.5f}".rstrip("0").rstrip(".") for v in coords))
    path = element(group, "path", d=" ".join(commands), opacity=opacity, data_text=text)
    element(path, "title").text = text
    ctx.new_path()


def arc(group, x, y, r, start, end, width, opacity, color):
    a, b = math.radians(start), math.radians(end)
    x0, y0 = x + r * math.cos(a), y + r * math.sin(a)
    x1, y1 = x + r * math.cos(b), y + r * math.sin(b)
    element(group, "path", d=f"M{x0:.5f} {y0:.5f} A{r} {r} 0 {int(end-start>180)} 1 {x1:.5f} {y1:.5f}", fill="none", stroke=color, stroke_width=width, opacity=opacity)


def overlay(layout, style, logo_path):
    w, h = style["canvas"]
    root = ET.Element(f"{{{NS}}}svg", {"viewBox": f"0 0 {w} {h}", "width": str(w), "height": str(h)})
    element(root, "title").text = f"{layout['title']} — deterministic lettering and original Omarchy wordmark"
    ink, accent = style["ink"], style["accent"]
    labels = element(root, "g", id="lettering", fill=ink)
    ctx = cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1))
    ctx.select_font_face(style["font_family"], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    options = cairo.FontOptions()
    options.set_hint_style(cairo.HINT_STYLE_NONE)
    options.set_hint_metrics(cairo.HINT_METRICS_OFF)
    ctx.set_font_options(options)
    x, y, width = style["legend"]["x"], style["legend"]["title_y"], style["legend"]["width"]
    outlined_text(ctx, labels, layout["title"], x, y, 25, 13.364, 0.95, max_width=width)
    element(root, "line", x1=x, y1=y+11, x2=x+width, y2=y+11, stroke=ink, stroke_width=0.75, opacity=0.65)
    outlined_text(ctx, labels, layout["subtitle"], x, y+32, 11, 6.012, 0.90, max_width=width)
    outlined_text(ctx, labels, layout["function"], x, y+54, 9, 2.052, 0.90, max_width=width)
    outlined_text(ctx, labels, "REQUIRED BREAKTHROUGHS", x, y+90, 9, 2.047, 0.85, max_width=width)
    outlined_text(ctx, labels, layout["breakthroughs"], x, y+110, 8.5, 2.637, 0.90, max_width=width)
    outlined_text(ctx, labels, layout["date"], x, y+129, 9, 4.019, 0.88, max_width=width)
    outlined_text(ctx, labels, layout["note"], x, y+150, 9, 2.623, 0.90, max_width=width)
    outlined_text(ctx, labels, layout["code"], style["code"]["right"], style["code"]["baseline"], 9, 2, 0.85, right=True, max_width=240)
    for label in layout.get("labels", []):
        outlined_text(ctx, labels, label["text"], label["x"], label["y"], 8.3, 1.6, label.get("opacity", 0.90))

    e = style["emblem"]
    cx, cy = e["center"]
    r = e["radius"]
    seal = element(root, "g", id="omarchy-emblem")
    for offset in [0, 120, 240]:
        arc(seal, cx, cy, r, offset+7, offset+95, 0.6, 0.35, ink)
        arc(seal, cx, cy, r-6, offset+17, offset+76, 2.2, 0.72, ink)
        arc(seal, cx, cy, r-12, offset-6, offset+99, 0.55, 0.50, ink)
    arc(seal, cx, cy, r-18, 202, 285, 1.1, 0.80, accent)
    element(seal, "circle", cx=cx, cy=cy, r=r-24, fill="none", stroke=ink, stroke_width=0.7, opacity=0.65)
    for angle in [35, 155, 275]:
        a = math.radians(angle)
        element(seal, "circle", cx=f"{cx+r*math.cos(a):.5f}", cy=f"{cy+r*math.sin(a):.5f}", r=1.25, fill=ink, opacity=0.78)
    # Copy original path data, preserving fill rules and the source aspect ratio.
    logo = ET.parse(logo_path).getroot()
    vx, vy, vw, vh = map(float, logo.attrib["viewBox"].split())
    scale = e["logo_width"] / vw
    wordmark = element(seal, "g", id="omarchy-wordmark", fill=ink, opacity=0.98,
                       transform=f"translate({cx-e['logo_width']/2:.5f} {cy-vh*scale/2:.5f}) scale({scale:.10f}) translate({-vx:g} {-vy:g})")
    for original in logo.iter(f"{{{NS}}}path"):
        path = copy.deepcopy(original)
        path.attrib.pop("fill", None)
        wordmark.append(path)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def cleanup(source, settings):
    """Clone clean grain into reserved type areas, keeping all other art intact.

    Text inpainting left dark glyph-shaped halos in this source. Replace the
    complete reserved rectangles instead, using actual grain sampled from an
    empty area and a color plane fitted to each rectangle's surrounding ground.
    """
    import cv2
    rgb = np.asarray(source.convert("RGB")).copy()
    mask = np.zeros(rgb.shape[:2], dtype=np.uint8)
    repaired = rgb.copy()
    tx0, ty0, tx1, ty1 = settings["texture_source"]
    texture = rgb[ty0:ty1, tx0:tx1].astype(np.float32)
    texture -= cv2.GaussianBlur(texture, (0, 0), 7)
    texture = np.concatenate([texture, texture[:, ::-1]], axis=1)
    texture = np.concatenate([texture, texture[::-1]], axis=0)
    h, w = rgb.shape[:2]
    for i, (x0, y0, x1, y1) in enumerate(settings["regions"]):
        rw, rh = x1-x0, y1-y0
        border = settings["border_width"]
        sx0, sy0, sx1, sy1 = max(0, x0-border), max(0, y0-border), min(w, x1+border), min(h, y1+border)
        by, bx = np.mgrid[sy0:sy1, sx0:sx1]
        surround = rgb[sy0:sy1, sx0:sx1].astype(np.float32)
        valid = ((bx < x0) | (bx >= x1) | (by < y0) | (by >= y1)) & (surround.mean(axis=2) < settings["background_threshold"])
        basis = np.stack([np.ones_like(bx), (bx-x0)/rw, (by-y0)/rh], axis=-1)
        plane, *_ = np.linalg.lstsq(basis[valid], surround[valid], rcond=None)
        yy, xx = np.mgrid[:rh, :rw]
        ground = np.stack([np.ones_like(xx), xx/rw, yy/rh], axis=-1) @ plane
        grain = texture[(yy+i*23) % texture.shape[0], (xx+i*37) % texture.shape[1]]
        patch = np.clip(ground+grain, 0, 255)
        distance = np.minimum.reduce([xx+1, yy+1, rw-xx, rh-yy])
        alpha = np.minimum(1, distance/settings["feather"])[..., None]
        repaired[y0:y1, x0:x1] = np.rint(patch*alpha + rgb[y0:y1, x0:x1]*(1-alpha)).astype(np.uint8)
        mask[y0:y1, x0:x1] = 255
    if not np.array_equal(repaired[mask == 0], rgb[mask == 0]):
        raise RuntimeError("Cleanup modified pixels outside the approved mask")
    return Image.fromarray(repaired), Image.fromarray(mask)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("layout", type=Path)
    parser.add_argument("--out", type=Path, help="Output prefix; defaults beside the layout")
    parser.add_argument("--size", help="Export WIDTHxHEIGHT; Lanczos for art, native vector rendering for lettering; centered crop without stretching")
    parser.add_argument("--restored-art", type=Path, help="AI-restored, text-free artwork in exactly the original aspect ratio")
    parser.add_argument("--restoration-record", type=Path, help="JSON provenance containing input_sha256 and output_sha256")
    parser.add_argument("--retain-grain", type=float, default=0, help="Retain 0..1 of original high-frequency texture in dark, low-gradient areas after AI restoration")
    args = parser.parse_args()
    if bool(args.restored_art) != bool(args.restoration_record):
        parser.error("--restored-art and --restoration-record must be supplied together")
    if not 0 <= args.retain_grain <= 1 or (args.retain_grain and not args.restored_art):
        parser.error("--retain-grain must be between 0 and 1 and requires --restored-art")
    layout_path = args.layout.resolve()
    layout = json.loads(layout_path.read_text())
    style_path = ROOT / "tools/blueprint-style.json"
    style = json.loads(style_path.read_text())
    source_path = layout_path.parent / layout["source"]
    logo_path = ROOT / "tools/omarchy-logo.svg"
    for key, pattern in [("font_regular", style["font_family"]), ("font_bold", style["font_family"]+":style=Bold")]:
        resolved = subprocess.check_output(["fc-match", "-f", "%{file}", pattern], text=True)
        if Path(resolved).resolve() != Path(style[key]).resolve():
            raise RuntimeError(f"Unexpected font substitution: {pattern} resolved to {resolved}")
    target = tuple(style["canvas"])
    if args.size:
        try:
            target = tuple(int(v) for v in args.size.lower().split("x"))
            if len(target) != 2 or min(target) < 1:
                raise ValueError
        except ValueError:
            parser.error("--size must be positive WIDTHxHEIGHT")
    stem = layout_path.name.replace(".layout.json", "")
    if args.size:
        stem += f"-{target[0]}x{target[1]}"
    prefix = args.out or layout_path.with_name(stem)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    def output(suffix):
        return Path(str(prefix) + suffix)
    source = Image.open(source_path).convert("RGB")
    expected_canvas = layout.get("source_canvas", style["canvas"])
    if list(source.size) != expected_canvas:
        raise ValueError(f"Expected art canvas {expected_canvas}, got {source.size}; do not silently stretch the drawing")
    if layout.get("cleanup"):
        art, mask = cleanup(source, layout["cleanup"])
        mask.save(output(".cleanup-mask.png"))
    else:
        art = source
    native_width, native_height = art.size
    clean_reference = art
    restoration = None
    if args.restored_art:
        restoration = json.loads(args.restoration_record.read_text())
        clean_bytes = io.BytesIO()
        art.save(clean_bytes, format="PNG")
        if hashlib.sha256(clean_bytes.getvalue()).hexdigest() != restoration["input_sha256"]:
            raise ValueError("AI input does not match the current clean artwork")
        if digest(args.restored_art) != restoration["output_sha256"]:
            raise ValueError("Restored artwork hash does not match its provenance")
        art = Image.open(args.restored_art).convert("RGB")
        if art.width * native_height != art.height * native_width:
            raise ValueError("Restored artwork aspect ratio differs from the original")
        if art.width <= native_width:
            raise ValueError("Restored artwork must have higher resolution than the source")
    scale = max(target[0]/native_width, target[1]/native_height)
    visible_width, visible_height = target[0]/scale, target[1]/scale
    left, top = (native_width-visible_width)/2, (native_height-visible_height)/2
    crop = (left, top, left+visible_width, top+visible_height)
    if target != art.size:
        source_scale = art.width/native_width
        art = art.resize(target, Image.Resampling.LANCZOS, box=tuple(v*source_scale for v in crop))
    if args.retain_grain:
        import cv2
        luminance = np.asarray(clean_reference.convert("L"), dtype=np.float32)
        residual = luminance-cv2.GaussianBlur(luminance, (0, 0), 1.25)
        smooth = cv2.GaussianBlur(luminance, (0, 0), 0.7)
        gx = cv2.Sobel(smooth, cv2.CV_32F, 1, 0, ksize=3)/8
        gy = cv2.Sobel(smooth, cv2.CV_32F, 0, 1, ksize=3)/8
        gradient = cv2.dilate(np.hypot(gx, gy), np.ones((7, 7), np.uint8))
        quiet = ((gradient < 5) & (luminance < 65)).astype(np.float32)
        quiet = cv2.GaussianBlur(quiet, (0, 0), 1.5)
        # Restore existing grain only, not the original blurred object contours.
        grain = Image.fromarray(residual*quiet).resize(target, Image.Resampling.LANCZOS, box=crop)
        rgb = np.asarray(art, dtype=np.float32)
        rgb += np.asarray(grain)[:, :, None]*args.retain_grain
        art = Image.fromarray(np.clip(np.rint(rgb), 0, 255).astype(np.uint8))
    art.save(output(".art.png"))
    svg_path = output(".overlay.svg")
    vector = ET.fromstring(overlay(layout, style, logo_path))
    # Artwork can now arrive at native 4K. Keep branding in the shared design
    # coordinates, regardless of source pixel count or a slightly different ratio.
    design_width, design_height = style["canvas"]
    vector_scale = max(target[0]/design_width, target[1]/design_height)
    vector_width, vector_height = target[0]/vector_scale, target[1]/vector_scale
    vector_left, vector_top = (design_width-vector_width)/2, (design_height-vector_height)/2
    vector.set("viewBox", f"{vector_left:.10f} {vector_top:.10f} {vector_width:.10f} {vector_height:.10f}")
    vector.set("width", str(target[0]))
    vector.set("height", str(target[1]))
    svg_path.write_bytes(ET.tostring(vector, encoding="utf-8", xml_declaration=True))
    png = subprocess.check_output(["rsvg-convert", str(svg_path)])
    output(".overlay.png").write_bytes(png)
    layer = Image.open(io.BytesIO(png)).convert("RGBA")
    composed = Image.alpha_composite(art.convert("RGBA"), layer).convert("RGB")
    composed.save(output(".composed.png"))
    composed.save(output(".composed.webp"), lossless=True, method=6)
    sources = {"art_source": source_path, "layout": layout_path, "style": style_path, "logo": logo_path,
               "font_regular": Path(style["font_regular"]), "font_bold": Path(style["font_bold"]), "compositor": Path(__file__)}
    if restoration:
        sources.update(restored_art=args.restored_art, restoration_record=args.restoration_record)
    report = {
        "canvas": list(target),
        "source_canvas": list(source.size),
        "design_canvas": style["canvas"],
        "art_export": {"filter": "Lanczos downsample after AI" if restoration else ("Lanczos" if target != source.size else "none"), "scale": scale, "source_crop_box": crop, "ai_super_resolution": bool(restoration), "restoration": restoration, "original_grain_retention": args.retain_grain},
        "source_sha256": {k: digest(v) for k, v in sources.items()},
        "output_sha256": {suffix: digest(output(suffix)) for suffix in [".art.png", ".overlay.svg", ".overlay.png", ".composed.png", ".composed.webp"]},
        "typography": "All text is outlined vector geometry. Logo path data is copied from the original SVG without redrawing.",
        "determinism": "Exact bytes verified within the recorded renderer environment; preserve the final outlined SVG to avoid font-version drift.",
        "renderer": {"cairo": cairo.cairo_version_string(), "librsvg": subprocess.check_output(["rsvg-convert", "--version"], text=True).strip()},
    }
    output(".build.json").write_text(json.dumps(report, indent=2) + "\n")
    print(output(".composed.png"))


if __name__ == "__main__":
    main()
