#!/usr/bin/env python3
import math
import os
import sys

INK = "#23262c"
EDGE = "#ffffff"
ACCENT = "#3a8ee6"
EW = 1.7

ARROW = "M5 3 L5 19.2 L9 15.7 L11.6 21.1 L13.7 20.1 L11.2 14.8 L16.6 14.8 Z"
HAND = ("M9 4.6 Q9 3.4 10.2 3.4 Q11.4 3.4 11.4 4.6 L11.4 10.6 Q11.6 9.7 12.6 9.7 Q13.6 9.8 13.7 10.8 "
        "Q14 10.2 14.8 10.2 Q15.8 10.3 15.9 11.3 Q16.2 10.8 16.9 10.8 Q18 10.9 18 12.1 L18 16.4 "
        "Q18 20.8 13.9 20.8 L12.4 20.8 Q10.3 20.8 9.1 19.1 L6.2 15.1 Q5.7 14.2 6.4 13.7 Q7.2 13.2 7.9 13.9 L9 15 Z")
OPEN = ("M7.6 12.8 L7.6 7 Q7.6 6 8.6 6 Q9.6 6 9.6 7 L9.6 11 L9.9 5 Q9.9 4 10.9 4 Q11.9 4 11.9 5 "
        "L11.9 10.9 L12.2 5.7 Q12.2 4.7 13.2 4.7 Q14.2 4.7 14.2 5.7 L14.2 11.2 L14.6 7.6 Q14.7 6.7 15.6 6.7 "
        "Q16.6 6.8 16.6 7.8 L16.6 15.2 Q16.6 20.6 12 20.6 L11.2 20.6 Q8.9 20.6 7.6 18.6 L5.2 15 Q4.7 14.1 5.4 13.6 "
        "Q6.1 13.1 6.8 13.8 Z")
FIST = ("M7.6 11.4 Q7.6 9.6 9.2 9.6 Q10.2 9.6 10.6 10.3 Q11 9.3 12.2 9.3 Q13.3 9.3 13.7 10.2 Q14.2 9.6 15 9.6 "
        "Q16.6 9.7 16.6 11.5 L16.6 15.4 Q16.6 20.6 12 20.6 L11.4 20.6 Q9.1 20.6 7.8 18.7 L6.2 16.3 Q5.7 15.4 6.4 14.8 "
        "Q7.1 14.3 7.6 14.9 Z")
L_IBEAM = "M9 4.2 Q11 4.2 12 5.4 Q13 4.2 15 4.2 M12 5.4 V18.6 M9 19.8 Q11 19.8 12 18.6 Q13 19.8 15 19.8"
L_EW = "M5.4 12 H18.6"
H_EW = "M4.6 12 L8.2 9 L8.2 15 Z M19.4 12 L15.8 9 L15.8 15 Z"
L_COL = "M4.6 12 H9.2 M14.8 12 H19.4 M10.6 5.6 V18.4 M13.4 5.6 V18.4"
H_COL = "M3.8 12 L7 9.4 L7 14.6 Z M20.2 12 L17 9.4 L17 14.6 Z"
L_EDGE = "M12 20 V8"
H_EDGE = "M12 6 L15 9.6 L9 9.6 Z"
B_EDGE = "M6.2 3.6 H17.8"
L_DIAG = "M7.6 7.6 L16.4 16.4"
H_DIAG = "M5.6 5.6 L10.4 6.3 L6.3 10.4 Z M18.4 18.4 L13.6 17.7 L17.7 13.6 Z"
L_CORNER = "M17.6 17.6 L8.8 8.8"
H_CORNER = "M6.8 6.8 L11.6 7.5 L7.5 11.6 Z"
B_CORNER = "M3.6 9.6 V3.6 H9.6"
L_FOUR = "M12 6.2 V17.8 M6.2 12 H17.8"
H_FOUR = ("M12 3.4 L14.8 6.6 L9.2 6.6 Z M12 20.6 L14.8 17.4 L9.2 17.4 Z "
          "M3.4 12 L6.6 9.2 L6.6 14.8 Z M20.6 12 L17.4 9.2 L17.4 14.8 Z")
L_CROSS = "M12 3.6 V9.4 M12 14.6 V20.4 M3.6 12 H9.4 M14.6 12 H20.4"
L_CELL = "M12 5.6 V18.4 M5.6 12 H18.4"
L_X = "M7 7 L17 17 M17 7 L7 17"


def shadow_defs():
    return ('<filter id="s" filterUnits="userSpaceOnUse" x="-2" y="-2" width="28" height="28">'
            '<feDropShadow dx="0" dy="0.5" stdDeviation="0.6" flood-color="#000" flood-opacity="0.35"/></filter>')


def body(d, transform=""):
    t = f' transform="{transform}"' if transform else ""
    return (f'<g filter="url(#s)"{t}><path d="{d}" fill="{EDGE}" stroke="{EDGE}" stroke-width="{EW}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="{INK}"/></g>')


def lines(d, width, heads=None, transform=""):
    t = f' transform="{transform}"' if transform else ""
    out = f'<g filter="url(#s)"{t}><path d="{d}" fill="none" stroke="{EDGE}" stroke-width="{width + EW}" stroke-linecap="round" stroke-linejoin="round"/>'
    if heads:
        out += f'<path d="{heads}" fill="{EDGE}" stroke="{EDGE}" stroke-width="{EW}" stroke-linejoin="round"/>'
    out += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
    if heads:
        out += f'<path d="{heads}" fill="{INK}"/>'
    return out + "</g>"


def svg(content, size=24):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24">'
            f'<defs>{shadow_defs()}</defs>{content}</svg>\n')


def badge(inner):
    cx, cy, r = 17.8, 17.8, 4.2
    return (f'<g filter="url(#s)"><circle cx="{cx}" cy="{cy}" r="{r + EW / 2}" fill="{EDGE}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{INK}"/>{inner}</g>')


def plus_badge():
    return badge(f'<path d="M17.8 15.9 V19.7 M15.9 17.8 H19.7" stroke="{EDGE}" stroke-width="1.2" stroke-linecap="round"/>')


def link_badge():
    return badge(f'<path d="M15.9 19.4 Q15.9 16.6 18.6 16.6 M17.6 15.4 L18.9 16.6 L17.6 17.8" fill="none" stroke="{EDGE}" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/>')


def help_badge():
    return badge(f'<path d="M16.4 16.8 Q16.4 15.3 17.8 15.3 Q19.2 15.3 19.2 16.5 Q19.2 17.3 18.4 17.7 Q17.8 18 17.8 18.6" fill="none" stroke="{EDGE}" stroke-width="1.1" stroke-linecap="round"/>'
                 f'<circle cx="17.8" cy="20" r="0.65" fill="{EDGE}"/>')


def menu_badge():
    return badge(f'<path d="M16 16.3 H19.6 M16 17.8 H19.6 M16 19.3 H19.6" stroke="{EDGE}" stroke-width="0.9" stroke-linecap="round"/>')


def forbid(cx, cy, r, w):
    a = math.radians(45)
    x1, y1 = cx - r * math.cos(a), cy + r * math.sin(a)
    x2, y2 = cx + r * math.cos(a), cy - r * math.sin(a)
    return (f'<g filter="url(#s)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{EDGE}" stroke-width="{w + EW}"/>'
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{EDGE}" stroke-width="{w + EW}" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="{w}"/>'
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="{w}" stroke-linecap="round"/></g>')


def nodrop_badge():
    return forbid(17.8, 17.8, 3.4, 1.4)


def spinner(cx, cy, r, w, frame, frames):
    start = frame * 360 / frames - 90
    sweep = 100
    a0, a1 = math.radians(start), math.radians(start + sweep)
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    return (f'<g filter="url(#s)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{EDGE}" stroke-width="{w + EW}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="{w}"/>'
            f'<path d="M{x0:.3f} {y0:.3f} A{r} {r} 0 0 1 {x1:.3f} {y1:.3f}" fill="none" stroke="{ACCENT}" stroke-width="{w}" stroke-linecap="round"/></g>')


def magnifier(sign):
    out = (f'<g filter="url(#s)"><line x1="14.4" y1="14.4" x2="19.6" y2="19.6" stroke="{EDGE}" stroke-width="{2.4 + EW}" stroke-linecap="round"/>'
           f'<circle cx="10.2" cy="10.2" r="5.6" fill="none" stroke="{EDGE}" stroke-width="{1.6 + EW}"/>'
           f'<circle cx="10.2" cy="10.2" r="5.6" fill="{EDGE}" fill-opacity="0.001"/>'
           f'<line x1="14.4" y1="14.4" x2="19.6" y2="19.6" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>'
           f'<circle cx="10.2" cy="10.2" r="5.6" fill="none" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M7.8 10.2 H12.6" stroke="{INK}" stroke-width="1.4" stroke-linecap="round"/>')
    if sign == "+":
        out += f'<path d="M10.2 7.8 V12.6" stroke="{INK}" stroke-width="1.4" stroke-linecap="round"/>'
    return out + "</g>"


SPIN_FRAMES = 12


def cursors():
    c = {}
    hot = (5, 3)
    c["default"] = ([body(ARROW)], hot)
    c["context-menu"] = ([body(ARROW), menu_badge()], hot)
    c["help"] = ([body(ARROW), help_badge()], hot)
    c["copy"] = ([body(ARROW), plus_badge()], hot)
    c["alias"] = ([body(ARROW), link_badge()], hot)
    c["no-drop"] = ([body(ARROW), nodrop_badge()], hot)
    c["progress"] = ([[body(ARROW), spinner(17.6, 17.6, 3.3, 1.5, f, SPIN_FRAMES)] for f in range(SPIN_FRAMES)], hot)
    c["wait"] = ([[spinner(12, 12, 6.6, 2, f, SPIN_FRAMES)] for f in range(SPIN_FRAMES)], (12, 12))
    c["pointer"] = ([body(HAND)], (10.2, 3.5))
    c["grab"] = ([body(OPEN)], (11.5, 11))
    c["grabbing"] = ([body(FIST)], (12, 12))
    c["text"] = ([lines(L_IBEAM, 1.4)], (12, 12))
    c["vertical-text"] = ([lines(L_IBEAM, 1.4, transform="rotate(90 12 12)")], (12, 12))
    c["crosshair"] = ([lines(L_CROSS, 1.3)], (12, 12))
    c["cell"] = ([lines(L_CELL, 2.6)], (12, 12))
    c["not-allowed"] = ([forbid(12, 12, 6.8, 2)], (12, 12))
    for name in ("all-scroll", "all-resize", "move"):
        c[name] = ([lines(L_FOUR, 1.4, H_FOUR)], (12, 12))
    c["ew-resize"] = ([lines(L_EW, 1.4, H_EW)], (12, 12))
    c["ns-resize"] = ([lines(L_EW, 1.4, H_EW, "rotate(90 12 12)")], (12, 12))
    c["nwse-resize"] = ([lines(L_DIAG, 1.4, H_DIAG)], (12, 12))
    c["nesw-resize"] = ([lines(L_DIAG, 1.4, H_DIAG, "rotate(90 12 12)")], (12, 12))
    c["col-resize"] = ([lines(L_COL, 1.4, H_COL)], (12, 12))
    c["row-resize"] = ([lines(L_COL, 1.4, H_COL, "rotate(90 12 12)")], (12, 12))
    edge = lambda t: lines(L_EDGE, 1.4, H_EDGE, t) + lines(B_EDGE, 1.4, None, t)
    c["n-resize"] = ([edge("")], (12, 3.6))
    c["e-resize"] = ([edge("rotate(90 12 12)")], (20.4, 12))
    c["s-resize"] = ([edge("rotate(180 12 12)")], (12, 20.4))
    c["w-resize"] = ([edge("rotate(270 12 12)")], (3.6, 12))
    corner = lambda t: lines(L_CORNER, 1.4, H_CORNER, t) + lines(B_CORNER, 1.4, None, t)
    c["nw-resize"] = ([corner("")], (3.6, 3.6))
    c["ne-resize"] = ([corner("rotate(90 12 12)")], (20.4, 3.6))
    c["se-resize"] = ([corner("rotate(180 12 12)")], (20.4, 20.4))
    c["sw-resize"] = ([corner("rotate(270 12 12)")], (3.6, 20.4))
    c["zoom-in"] = ([magnifier("+")], (10.2, 10.2))
    c["zoom-out"] = ([magnifier("-")], (10.2, 10.2))
    c["X_cursor"] = ([lines(L_X, 1.8)], (12, 12))
    return c


ALIASES = {
    "left_ptr": "default", "arrow": "default", "top_left_arrow": "default", "dnd-move": "default",
    "dnd-ask": "context-menu", "question_arrow": "help", "whats_this": "help",
    "dnd-copy": "copy", "dnd-link": "alias", "link": "alias",
    "dnd-none": "no-drop", "dnd-no-drop": "no-drop", "circle": "not-allowed", "crossed_circle": "not-allowed",
    "left_ptr_watch": "progress", "half-busy": "progress", "watch": "wait",
    "hand2": "pointer", "hand1": "grab", "openhand": "grab", "closedhand": "grabbing",
    "xterm": "text", "ibeam": "text", "cross": "crosshair", "tcross": "crosshair", "cross_reverse": "crosshair",
    "diamond_cross": "crosshair", "plus": "cell", "fleur": "all-scroll", "size_all": "all-scroll",
    "sb_h_double_arrow": "ew-resize", "h_double_arrow": "ew-resize", "size_hor": "ew-resize",
    "sb_v_double_arrow": "ns-resize", "v_double_arrow": "ns-resize", "size_ver": "ns-resize",
    "bd_double_arrow": "nwse-resize", "size_fdiag": "nwse-resize", "fd_double_arrow": "nesw-resize", "size_bdiag": "nesw-resize",
    "split_h": "col-resize", "sb_h_double_arrow_split": "col-resize", "split_v": "row-resize",
    "top_side": "n-resize", "right_side": "e-resize", "bottom_side": "s-resize", "left_side": "w-resize",
    "top_left_corner": "nw-resize", "top_right_corner": "ne-resize", "bottom_right_corner": "se-resize",
    "bottom_left_corner": "sw-resize", "pirate": "X_cursor", "x-cursor": "X_cursor",
    "forbidden": "not-allowed", "pointing_hand": "pointer",
    "3085a0e285430894940527032f8b26df": "alias", "640fb0e74195791501fd1ed57b41487f": "alias",
    "1081e37283d90000800003c07f3ef6bf": "copy", "6407b0e94181790501fd1e167b474872": "copy",
    "08e8e1c95fe2fc01f976f1e063a24ccd": "progress", "3ecb610c1bf2410f44200f48c40d3599": "progress",
    "d9ce0ab605698f320427677b458ad60b": "help", "5c6cd98b3f3ebcb1f9c7f1c204630408": "help",
    "9d800788f1b08800ae810202380a0822": "pointer", "e29285e634086352946a0e7090d73106": "pointer",
    "00008160000006810000408080010102": "ns-resize", "028006030e0e7ebffc7f7070c0600140": "ew-resize",
    "c7088f0f3e6c8088236ef8e1e3e70000": "nwse-resize", "fcf1c3c7cd4491d801f1e1c78f100000": "nesw-resize",
    "14fef782d02440884392942c11205230": "col-resize", "2870a09082c103050810ffdffffe0204": "row-resize",
    "03b6e0fcb3499374a867c041f52298f0": "not-allowed", "4498f0e0c1937ffe01fd06f973665830": "all-scroll",
    "9081237383d90e509aa00f00170e968f": "all-scroll", "fcf21c00b30f7e3f83fe0dfd12e71cff": "grabbing",
}

def main_to(out):
    os.makedirs(out, exist_ok=True)
    for name, (frames, hot) in cursors().items():
        if isinstance(frames[0], list):
            for i, parts in enumerate(frames):
                open(os.path.join(out, f"{name}-{i:02d}.svg"), "w").write(svg("".join(parts)))
        else:
            open(os.path.join(out, f"{name}.svg"), "w").write(svg("".join(frames)))
        open(os.path.join(out, f"{name}.hot"), "w").write(f"{hot[0]} {hot[1]}\n")

if __name__ == "__main__":
    main_to(sys.argv[1])
