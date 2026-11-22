#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
import tempfile

import draw
import motion

SIZES = (24, 32, 48, 64, 96)


def frame_delay(index, count, loops):
    if count == 1:
        return ""
    return f" {0 if index == count - 1 and not loops else motion.STEP}"


def write_cursor(tmp, cursors_dir, name, frames, hot, loops):
    lines = []
    for i, frame in enumerate(frames):
        src = os.path.join(tmp, f"{name}-{i}.svg")
        with open(src, "w") as f:
            f.write(draw.svg(frame))
        for size in SIZES:
            png = os.path.join(tmp, f"{name}-{size}-{i}.png")
            subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), src, "-o", png], check=True)
            x = min(size - 1, round(hot[0] * size / 24))
            y = min(size - 1, round(hot[1] * size / 24))
            lines.append((size, i, f"{size} {x} {y} {png}{frame_delay(i, len(frames), loops)}"))
    config = os.path.join(tmp, f"{name}.cfg")
    with open(config, "w") as f:
        f.write("\n".join(line for *_, line in sorted(lines)) + "\n")
    subprocess.run(["xcursorgen", config, os.path.join(cursors_dir, name)], check=True)


def build(out_dir):
    cursors_dir = os.path.join(out_dir, "cursors")
    if os.path.lexists(cursors_dir):
        shutil.rmtree(cursors_dir)
    os.makedirs(cursors_dir)
    with tempfile.TemporaryDirectory() as tmp:
        for base, (_, hot) in draw.cursors().items():
            for name, frames, loops in motion.sequences(base):
                write_cursor(tmp, cursors_dir, name, frames, hot, loops)
    for alias, target in draw.ALIASES.items():
        path = os.path.join(cursors_dir, alias)
        if not os.path.lexists(path):
            os.symlink(target, path)


if __name__ == "__main__":
    build(sys.argv[1])
