#!/usr/bin/env python3
import argparse
import math
import configparser
import os
import shutil

TEMPLATE = {
    "back_depth": "#21628c",
    "back_mid": "#2c6c98",
    "back_top": "#00315f",
    "back_bot": "#001d3c",
    "front_depth": "#4889b3",
    "rim": "#71bcf1",
    "front": "#0b98bd",
    "glow_a": "#048cc4",
    "glow_b": "#03d1d6",
    "mark": "#e6f7ff",
    "mark_shade": "#06456d",
}

ACCENT_HEX = {
    "blue": "#3584e4",
    "teal": "#2190a4",
    "green": "#3a944a",
    "yellow": "#e5a50a",
    "orange": "#e66100",
    "red": "#e01b24",
    "pink": "#d56199",
    "purple": "#9141ac",
    "slate": "#787878",
}

HUE_FOLLOW = 0.35
MIN_CHROMA_RATIO = 0.15
NEUTRAL_CHROMA = 0.02


def _to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _to_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def hex_to_oklch(value):
    r, g, b = (_to_linear(int(value[i:i + 2], 16) / 255) for i in (1, 3, 5))
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    lightness = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return lightness, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def _oklch_to_linear(lightness, chroma, hue):
    a = chroma * math.cos(math.radians(hue))
    b = chroma * math.sin(math.radians(hue))
    l = (lightness + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (lightness - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (lightness - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def oklch_to_hex(lightness, chroma, hue):
    rgb = _oklch_to_linear(lightness, chroma, hue)
    for _ in range(80):
        if all(-0.0001 <= c <= 1.0001 for c in rgb):
            break
        chroma *= 0.95
        rgb = _oklch_to_linear(lightness, chroma, hue)
    return "#%02x%02x%02x" % tuple(round(max(0.0, min(1.0, _to_srgb(max(0.0, c)))) * 255) for c in rgb)


def palette_for(accent_hex):
    accent_l, accent_c, accent_h = hex_to_oklch(accent_hex)
    front_l, front_c, front_h = hex_to_oklch(TEMPLATE["front"])
    ratio = max(MIN_CHROMA_RATIO, min(1.0, accent_c / front_c))
    if accent_c < NEUTRAL_CHROMA:
        accent_h = front_h
    out = {}
    for key, value in TEMPLATE.items():
        lightness, chroma, hue = hex_to_oklch(value)
        offset = ((hue - front_h + 180) % 360) - 180
        out[key] = oklch_to_hex(lightness, chroma * ratio, accent_h + offset * HUE_FOLLOW)
    return out


ACCENTS = {name: palette_for(value) for name, value in ACCENT_HEX.items()}
ACCENTS["teal"] = dict(TEMPLATE)


def is_template(path):
    with open(path, encoding="utf-8") as f:
        text = f.read().lower()
    return TEMPLATE["front"] in text and TEMPLATE["back_top"] in text


def recolor(text, accent):
    out = text
    for key, value in TEMPLATE.items():
        out = out.replace(value, "\0" + key + "\0").replace(value.upper(), "\0" + key + "\0")
    for key, value in ACCENTS[accent].items():
        out = out.replace("\0" + key + "\0", value)
    return out


def scan(base):
    files, links = [], []
    for dirpath, _, names in os.walk(base):
        for name in sorted(names):
            if not name.endswith(".svg"):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, base)
            if os.path.islink(path):
                target = os.path.realpath(path)
                if os.path.isfile(target) and is_template(target):
                    links.append((rel, os.readlink(path)))
            elif is_template(path):
                files.append(rel)
    return sorted(files), sorted(links)


def write_index(base, dest, accent, dirs):
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    parser.read(os.path.join(base, "index.theme"), encoding="utf-8")
    name = parser.get("Icon Theme", "Name", fallback="Singularity")
    lines = [
        "[Icon Theme]",
        "Name=%s-%s" % (name, accent),
        "Comment=%s folders in the %s accent" % (name, accent),
        "Inherits=%s" % os.path.basename(os.path.normpath(base)),
        "Hidden=true",
        "Directories=%s" % ",".join(dirs),
        "",
    ]
    for d in dirs:
        lines.append("[%s]" % d)
        if parser.has_section(d):
            lines += ["%s=%s" % (k, v) for k, v in parser.items(d)]
        else:
            lines += ["Size=16", "MinSize=8", "MaxSize=512", "Type=Scalable"]
        lines.append("")
    with open(os.path.join(dest, "index.theme"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip("\n") + "\n")


def generate(base, dest, accent):
    files, links = scan(base)
    if not files:
        raise SystemExit("no accent template icons found in %s" % base)
    if os.path.lexists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    dirs = set()
    for rel in files:
        out = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(os.path.join(base, rel), encoding="utf-8") as f:
            text = f.read()
        with open(out, "w", encoding="utf-8") as f:
            f.write(recolor(text, accent))
        dirs.add(os.path.dirname(rel))
    for rel, target in links:
        out = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        os.symlink(target, out)
        if not os.path.exists(out):
            raise SystemExit("alias %s points outside the accent set" % rel)
        dirs.add(os.path.dirname(rel))
    write_index(base, dest, accent, sorted(dirs))


def install_path(path):
    if "MESON_INSTALL_DESTDIR_PREFIX" not in os.environ:
        return os.path.abspath(path)
    if os.path.isabs(path):
        return os.environ.get("DESTDIR", "") + path
    return os.path.join(os.environ["MESON_INSTALL_DESTDIR_PREFIX"], path)


def write_template(theme_dir):
    lines = ["[Accent Template]"] + ["%s=%s" % (k, v) for k, v in TEMPLATE.items()]
    lines += ["", "[Derivation]", "hue_follow=%s" % HUE_FOLLOW, "min_chroma_ratio=%s" % MIN_CHROMA_RATIO,
              "neutral_chroma=%s" % NEUTRAL_CHROMA]
    with open(os.path.join(theme_dir, "accent-template.ini"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Generate per-accent variants of the Singularity icon theme.")
    parser.add_argument("base", help="base icon theme directory")
    parser.add_argument("output", help="variant directory, or a parent directory when no accent is given")
    parser.add_argument("accent", nargs="?", help="accent name or #rrggbb color")
    args = parser.parse_args()
    base = os.path.abspath(args.base)
    output = install_path(args.output)
    if args.accent:
        if args.accent.startswith("#"):
            ACCENTS[args.accent] = palette_for(args.accent)
        elif args.accent not in ACCENTS:
            raise SystemExit("unknown accent %s" % args.accent)
        generate(base, output, args.accent)
        return
    name = os.path.basename(os.path.normpath(base))
    for accent in ACCENTS:
        generate(base, os.path.join(output, "%s-%s" % (name, accent)), accent)
    installed_base = os.path.join(output, name)
    if os.path.isdir(installed_base):
        write_template(installed_base)


if __name__ == "__main__":
    main()
