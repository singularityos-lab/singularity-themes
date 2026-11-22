#!/usr/bin/env python3
import math

import draw

STEP = 16


def keyed(t, *keys):
    if t <= keys[0][0]:
        return keys[0][1]
    for (a, u), (b, v) in zip(keys, keys[1:]):
        if t <= b:
            p = (t - a) / (b - a)
            return u + (v - u) * (1 - (1 - p) ** 3)
    return keys[-1][1]


def num(v):
    return f'{v:.3f}'.rstrip('0').rstrip('.')


def swap(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new)


def about(x, y, sx=1, sy=None, turn=0):
    sy = sx if sy is None else sy
    return f'translate({num(x)} {num(y)}) rotate({num(turn)}) scale({num(sx)} {num(sy)}) translate({num(-x)} {num(-y)})'


def group(content, transform):
    return f'<g transform="{transform}">{content}</g>'


def arrow(t):
    return group(draw.body(draw.ARROW), about(5, 3, 1, None, keyed(t, (0, 11), (110, -3), (200, 0))))


def menu(t):
    gap = keyed(t, (0, .7), (90, .7), (250, 1.8), (330, 1.5))
    marks = ' '.join(f'M16 {num(17.8 + i * gap)} H19.6' for i in (-1, 0, 1))
    return draw.body(draw.ARROW) + draw.badge(f'<path d="{marks}" stroke="{draw.EDGE}" stroke-width="0.9" stroke-linecap="round"/>')


def question(t):
    turn = keyed(t, (0, -38), (170, 14), (280, 0))
    drop = keyed(t, (0, 0), (90, -1.1), (230, .2), (320, 0))
    hook = 'M16.4 16.8 Q16.4 15.3 17.8 15.3 Q19.2 15.3 19.2 16.5 Q19.2 17.3 18.4 17.7 Q17.8 18 17.8 18.6'
    return draw.body(draw.ARROW) + draw.badge(
        f'<path d="{hook}" transform="{about(17.8, 18.6, 1, None, turn)}" fill="none" stroke="{draw.EDGE}" stroke-width="1.1" stroke-linecap="round"/>'
        f'<circle cx="17.8" cy="{num(20 + drop)}" r="0.65" fill="{draw.EDGE}"/>')


def duplicate(t):
    out = keyed(t, (0, 0), (170, 7), (340, 0))
    twin = f'<g opacity="{num(keyed(t, (0, 1), (260, 1), (340, 0)))}">{draw.body(draw.ARROW, f"translate({num(out)} 0)")}</g>'
    return twin + draw.body(draw.ARROW) + draw.plus_badge()


def shortcut(t):
    x = keyed(t, (0, -.9), (170, .9), (270, 0))
    y = keyed(t, (0, .7), (100, -.9), (270, 0))
    turn = keyed(t, (0, -55), (170, 12), (270, 0))
    mark = 'M15.9 19.4 Q15.9 16.6 18.6 16.6 M17.6 15.4 L18.9 16.6 L17.6 17.8'
    return draw.body(draw.ARROW) + draw.badge(
        f'<path d="{mark}" transform="translate({num(x)} {num(y)}) {about(17.6, 17.6, 1, None, turn)}" fill="none" '
        f'stroke="{draw.EDGE}" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/>')


def refused(t):
    y = keyed(t, (0, -4.5), (90, .5), (170, -1.6), (250, .2), (330, 0))
    return draw.body(draw.ARROW) + group(draw.nodrop_badge(), f'translate(0 {num(y)})')


def ring(cx, cy, r, w, start, sweep):
    a, b = math.radians(start - 90), math.radians(start - 90 + sweep)
    p = [cx + r * math.cos(a), cy + r * math.sin(a), cx + r * math.cos(b), cy + r * math.sin(b)]
    x0, y0, x1, y1 = (f'{v:.3f}' for v in p)
    return (f'<g filter="url(#s)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{draw.EDGE}" stroke-width="{w + draw.EW}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{draw.INK}" stroke-width="{w}"/>'
            f'<path d="M{x0} {y0} A{r} {r} 0 {int(sweep > 180)} 1 {x1} {y1}" fill="none" stroke="{draw.ACCENT}" stroke-width="{w}" stroke-linecap="round"/></g>')


def working(t):
    return draw.body(draw.ARROW) + ring(17.6, 17.6, 3.3, 1.5, 0, keyed(t, (0, 2), (240, 100)))


def working_loop(p):
    return draw.body(draw.ARROW) + ring(17.6, 17.6, 3.3, 1.5, 360 * p, 100)


def waiting(t):
    return ring(12, 12, 6.6, 2, 0, keyed(t, (0, 2), (240, 100)))


def waiting_loop(p):
    return ring(12, 12, 6.6, 2, 720 * p, 100 + 75 * (1 - math.cos(math.tau * p)))


def finger(top):
    return draw.body(swap(draw.HAND, 'M9 4.6 Q9 3.4 10.2 3.4 Q11.4 3.4 11.4 4.6',
                       f'M9 {num(top)} Q9 {num(top - 1.2)} 10.2 {num(top - 1.2)} Q11.4 {num(top - 1.2)} 11.4 {num(top)}'))


def point(t):
    return finger(keyed(t, (0, 9.2), (150, 4.1), (240, 4.6)))


def fingers(curl):
    a, b, c, d = [v * m for v, m in zip(curl, (3.6, 5.5, 5, 3.2))]
    s = swap(draw.OPEN, 'L7.6 7 Q7.6 6 8.6 6 Q9.6 6 9.6 7', f'L7.6 {num(7 + a)} Q7.6 {num(6 + a)} 8.6 {num(6 + a)} Q9.6 {num(6 + a)} 9.6 {num(7 + a)}')
    s = swap(s, 'L9.9 5 Q9.9 4 10.9 4 Q11.9 4 11.9 5', f'L9.9 {num(5 + b)} Q9.9 {num(4 + b)} 10.9 {num(4 + b)} Q11.9 {num(4 + b)} 11.9 {num(5 + b)}')
    s = swap(s, 'L12.2 5.7 Q12.2 4.7 13.2 4.7 Q14.2 4.7 14.2 5.7', f'L12.2 {num(5.7 + c)} Q12.2 {num(4.7 + c)} 13.2 {num(4.7 + c)} Q14.2 {num(4.7 + c)} 14.2 {num(5.7 + c)}')
    s = swap(s, 'L14.6 7.6 Q14.7 6.7 15.6 6.7 Q16.6 6.8 16.6 7.8', f'L14.6 {num(7.6 + d)} Q14.7 {num(6.7 + d)} 15.6 {num(6.7 + d)} Q16.6 {num(6.8 + d)} 16.6 {num(7.8 + d)}')
    return draw.body(s)


def open_hand(t):
    return fingers([keyed(t, (i * 45, 1), (i * 45 + 130, -.08), (i * 45 + 210, 0)) for i in range(4)])


def closing(t):
    if t >= 235:
        return group(draw.body(draw.FIST), about(12, 20.6, keyed(t, (235, 1.07), (310, 1)), keyed(t, (235, .93), (310, 1))))
    return fingers([keyed(t, ((3 - i) * 35, 0), ((3 - i) * 35 + 120, 1)) for i in range(4)])


def beam(half, curl, width=3):
    top, low = 12 - half, 12 + half
    a, b = num(top - 1.2 * curl), num(low + 1.2 * curl)
    l, li, ri, r = (num(12 + m * width) for m in (-1, -1 / 3, 1 / 3, 1))
    return draw.lines(f'M{l} {a} Q{li} {a} 12 {num(top)} Q{ri} {a} {r} {a} M12 {num(top)} V{num(low)} '
                   f'M{l} {b} Q{li} {b} 12 {num(low)} Q{ri} {b} {r} {b}', 1.4)


def unfold(t):
    return beam(keyed(t, (0, 5), (130, 6.9), (220, 6.6)), keyed(t, (0, -.6), (90, -.6), (230, 1.4), (310, 1)),
                keyed(t, (0, 1.6), (180, 3.3), (280, 3)))


def lie_down(t):
    return draw.lines(draw.L_IBEAM, 1.4, transform=f'rotate({num(keyed(t, (0, 0), (170, 99), (280, 90)))} 12 12)')


def reticle(gap, reach=8.4):
    return draw.lines(f'M12 {num(12 - reach)} V{num(12 - gap)} M12 {num(12 + gap)} V{num(12 + reach)} '
                   f'M{num(12 - reach)} 12 H{num(12 - gap)} M{num(12 + gap)} 12 H{num(12 + reach)}', 1.3)


def aim(t):
    return reticle(keyed(t, (0, 4.6), (160, 2.1), (260, 2.6)), keyed(t, (0, 9.8), (160, 7.6), (260, 8.4)))


def select_cell(t):
    across = keyed(t, (0, 2.2), (120, 6.9), (200, 6.4))
    down = keyed(t, (0, 1.3), (110, 1.3), (230, 6.9), (320, 6.4))
    return draw.lines(f'M12 {num(12 - down)} V{num(12 + down)} M{num(12 - across)} 12 H{num(12 + across)}', 2.6)


def barrier(t):
    s = draw.forbid(12, 12, 6.8, 2)
    turn = f'<line transform="rotate({num(keyed(t, (0, -70), (120, 9), (180, -4), (250, 0)))} 12 12)" '
    return s.replace('<line ', turn)


def crossing(t):
    a = keyed(t, (0, 30), (150, -6), (250, 0))
    pts = []
    for deg in (45 + a, 135 - a):
        x, y = 7.071 * math.cos(math.radians(deg)), 7.071 * math.sin(math.radians(deg))
        pts.append(f'M{num(12 - x)} {num(12 - y)} L{num(12 + x)} {num(12 + y)}')
    return draw.lines(' '.join(pts), 1.8)


def four(n, e, s, w):
    d = f'M12 {num(6.2 - n)} V{num(17.8 + s)} M{num(6.2 - w)} 12 H{num(17.8 + e)}'
    h = (f'M12 {num(3.4 - n)} L14.8 {num(6.6 - n)} L9.2 {num(6.6 - n)} Z M12 {num(20.6 + s)} L14.8 {num(17.4 + s)} L9.2 {num(17.4 + s)} Z '
         f'M{num(3.4 - w)} 12 L{num(6.6 - w)} 9.2 L{num(6.6 - w)} 14.8 Z M{num(20.6 + e)} 12 L{num(17.4 + e)} 9.2 L{num(17.4 + e)} 14.8 Z')
    return draw.lines(d, 1.4, h)


def compass(t):
    return four(*[keyed(t, (i * 55, 0), (i * 55 + 75, 1.7), (i * 55 + 175, 0)) for i in range(4)])


def expand(t):
    v = keyed(t, (0, -2), (160, .8), (260, 0))
    return four(v, v, v, v)


def lift(t):
    size = keyed(t, (0, .88), (140, 1.16), (300, 1))
    drop = keyed(t, (0, .5), (140, 1.8), (300, .5))
    s = draw.lines(draw.L_FOUR, 1.4, draw.H_FOUR).replace('url(#s)', 'url(#lift)')
    shadow = ('<filter id="lift" filterUnits="userSpaceOnUse" x="-2" y="-2" width="28" height="28">'
              f'<feDropShadow dx="0" dy="{num(drop)}" stdDeviation="0.6" flood-color="#000" flood-opacity="0.35"/></filter>')
    return shadow + group(s, about(12, 12, size))


def double(left, right, transform=''):
    return draw.lines(f'M{num(5.4 - left)} 12 H{num(18.6 + right)}', 1.4,
                   f'M{num(4.6 - left)} 12 L{num(8.2 - left)} 9 L{num(8.2 - left)} 15 Z '
                   f'M{num(19.4 + right)} 12 L{num(15.8 + right)} 9 L{num(15.8 + right)} 15 Z', transform)


def pull(t):
    v = keyed(t, (0, -2.6), (130, 1.8), (210, -.6), (290, 0))
    return double(v, v)


def piston(t):
    return double(keyed(t, (0, -3.4), (120, 1.6), (220, 0)), keyed(t, (0, -3.4), (100, -3.4), (220, 1.6), (320, 0)), 'rotate(90 12 12)')


def tilt(sign):
    def move(t):
        base = 90 if sign < 0 else 0
        turn = base + keyed(t, (0, -45 * sign), (170, 7 * sign), (270, 0))
        return draw.lines(draw.L_DIAG, 1.4, draw.H_DIAG, f'rotate({num(turn)} 12 12)')
    return move


def split(bars, arms, transform=''):
    return draw.lines(f'M{num(4.6 - arms)} 12 H{num(9.2 - bars)} M{num(14.8 + bars)} 12 H{num(19.4 + arms)} '
                   f'M{num(10.6 - bars)} 5.6 V18.4 M{num(13.4 + bars)} 5.6 V18.4', 1.4,
                   f'M{num(3.8 - arms)} 12 L{num(7 - arms)} 9.4 L{num(7 - arms)} 14.6 Z '
                   f'M{num(20.2 + arms)} 12 L{num(17 + arms)} 9.4 L{num(17 + arms)} 14.6 Z', transform)


def part_columns(t):
    v = keyed(t, (0, -1.4), (150, .8), (260, 0))
    return split(v, v)


def spread_rows(t):
    bars = keyed(t, (0, .9), (110, -1.1), (290, 0))
    arms = keyed(t, (0, -1.6), (110, -1.6), (230, .9), (310, 0))
    return split(bars, arms, 'rotate(90 12 12)')


def push(turn):
    def move(t):
        y = keyed(t, (0, 2.6), (120, -.5), (240, 0))
        bend = keyed(t, (90, 0), (140, -2.2), (200, .7), (280, 0))
        tr = f'rotate({turn} 12 12)' if turn else ''
        return (draw.lines(f'M12 20 V{num(8 + y)}', 1.4, f'M12 {num(6 + y)} L15 {num(9.6 + y)} L9 {num(9.6 + y)} Z', tr)
                + draw.lines(f'M6.2 3.6 Q12 {num(3.6 + bend)} 17.8 3.6', 1.4, None, tr))
    return move


def stretch_corner(turn):
    def move(t):
        arm = keyed(t, (0, 3.2), (80, 3.2), (210, 7.2), (300, 6))
        back = keyed(t, (0, 1.4), (110, 1.9), (280, 0))
        size = keyed(t, (0, 1), (110, .95), (280, 1))
        tr = f'rotate({turn} 12 12)' if turn else ''
        arrow_d = f'M17.6 17.6 L{num(8.8 + back)} {num(8.8 + back)}'
        head = f'M{num(6.8 + back)} {num(6.8 + back)} L{num(11.6 + back)} {num(7.5 + back)} L{num(7.5 + back)} {num(11.6 + back)} Z'
        return (group(draw.lines(arrow_d, 1.4, head, tr), about(12, 12, size))
                + draw.lines(f'M3.6 {num(3.6 + arm)} V3.6 H{num(3.6 + arm)}', 1.4, None, tr))
    return move


def lens(size, sign, turn=0):
    s = draw.magnifier(sign)
    if sign == '+':
        s = swap(s, '<path d="M10.2 7.8 V12.6"', f'<path transform="rotate({num(turn)} 10.2 10.2)" d="M10.2 7.8 V12.6"')
    return group(s, about(10.2, 10.2, size))


def closer(t):
    return lens(keyed(t, (0, .72), (170, 1.12), (290, 1)), '+', keyed(t, (0, 90), (80, 90), (250, 0)))


def farther(t):
    return lens(keyed(t, (0, 1.12), (190, .88), (300, 1)), '-')


def press_arrow(t):
    return group(draw.body(draw.ARROW), about(5, 3, keyed(t, (0, 1), (80, .82))))


def press_finger(t):
    return finger(keyed(t, (0, 4.6), (90, 7.4)))


def press_grab(t):
    if t >= 120:
        return draw.body(draw.FIST)
    v = keyed(t, (0, 0), (112, 1))
    return fingers([v] * 4)


def press_text(t):
    return beam(keyed(t, (0, 6.6), (80, 5.3)), 1, keyed(t, (0, 3), (80, 2.3)))


def press_aim(t):
    return reticle(keyed(t, (0, 2.6), (80, 1.9)), keyed(t, (0, 8.4), (80, 7.1)))


def press_cell(t):
    return group(draw.lines(draw.L_CELL, 2.6), about(12, 12, keyed(t, (0, 1), (90, .76))))


ENTER = {
    "default": (arrow, 200),
    "context-menu": (menu, 330),
    "help": (question, 320),
    "copy": (duplicate, 340),
    "alias": (shortcut, 270),
    "no-drop": (refused, 330),
    "progress": (working, 240),
    "wait": (waiting, 240),
    "pointer": (point, 240),
    "grab": (open_hand, 345),
    "grabbing": (closing, 310),
    "text": (unfold, 310),
    "vertical-text": (lie_down, 280),
    "crosshair": (aim, 260),
    "cell": (select_cell, 320),
    "zoom-in": (closer, 290),
    "zoom-out": (farther, 300),
    "not-allowed": (barrier, 250),
    "X_cursor": (crossing, 250),
    "move": (lift, 300),
    "all-scroll": (compass, 340),
    "all-resize": (expand, 260),
    "ew-resize": (pull, 290),
    "ns-resize": (piston, 320),
    "nwse-resize": (tilt(1), 270),
    "nesw-resize": (tilt(-1), 270),
    "col-resize": (part_columns, 260),
    "row-resize": (spread_rows, 310),
    "n-resize": (push(0), 280),
    "e-resize": (push(90), 280),
    "s-resize": (push(180), 280),
    "w-resize": (push(270), 280),
    "nw-resize": (stretch_corner(0), 300),
    "ne-resize": (stretch_corner(90), 300),
    "se-resize": (stretch_corner(180), 300),
    "sw-resize": (stretch_corner(270), 300),
}
PRESS = {
    "default": (press_arrow, 80),
    "pointer": (press_finger, 90),
    "grab": (press_grab, 120),
    "text": (press_text, 80),
    "crosshair": (press_aim, 80),
    "cell": (press_cell, 90),
    "zoom-in": (lambda t: lens(keyed(t, (0, 1), (90, 1.12)), '+'), 90),
    "zoom-out": (lambda t: lens(keyed(t, (0, 1), (90, .8)), '-'), 90),
}
LOOPS = {"progress": (working_loop, 720), "wait": (waiting_loop, 1440)}


def rest(name):
    parts = draw.cursors()[name][0]
    return "".join(parts[0] if isinstance(parts[0], list) else parts)


def sequences(name):
    if name in LOOPS:
        spin, period = LOOPS[name]
        yield name, [spin(t / period) for t in range(0, period, STEP)], True
    else:
        yield name, [rest(name)], False
    move, end = ENTER[name]
    yield f"{name}-enter", [move(t) for t in range(0, end, STEP)] + [rest(name)], False
    if name in PRESS:
        press, end = PRESS[name]
        yield f"{name}-press", [press(t) for t in range(0, end, STEP)] + [press(end)], False
