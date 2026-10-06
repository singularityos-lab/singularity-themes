#!/usr/bin/env python3
import glob
import os
import shutil
import subprocess
import sys
import tempfile

import draw

SIZES = (24, 32, 48, 64, 96)
FRAME_MS = 60


def build(out_dir):
    cursors_dir = os.path.join(out_dir, "cursors")
    if os.path.lexists(cursors_dir):
        shutil.rmtree(cursors_dir)
    os.makedirs(cursors_dir)
    with tempfile.TemporaryDirectory() as tmp:
        svg_dir = os.path.join(tmp, "svg")
        draw.main_to(svg_dir)
        for name, (frames, hot) in draw.cursors().items():
            animated = isinstance(frames[0], list)
            sources = [os.path.join(svg_dir, f"{name}-{i:02d}.svg") for i in range(len(frames))] if animated else [os.path.join(svg_dir, f"{name}.svg")]
            lines = []
            for size in SIZES:
                scale = size / 24
                for i, src in enumerate(sources):
                    png = os.path.join(tmp, f"{name}-{size}-{i}.png")
                    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), src, "-o", png], check=True)
                    x = min(size - 1, round(hot[0] * scale))
                    y = min(size - 1, round(hot[1] * scale))
                    lines.append(f"{size} {x} {y} {png}" + (f" {FRAME_MS}" if animated else ""))
            config = os.path.join(tmp, f"{name}.cfg")
            with open(config, "w") as f:
                f.write("\n".join(lines) + "\n")
            subprocess.run(["xcursorgen", config, os.path.join(cursors_dir, name)], check=True)
    for alias, target in draw.ALIASES.items():
        path = os.path.join(cursors_dir, alias)
        if not os.path.lexists(path):
            os.symlink(target, path)


if __name__ == "__main__":
    build(sys.argv[1])
