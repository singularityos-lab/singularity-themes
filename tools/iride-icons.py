#!/usr/bin/env python3
import argparse
import concurrent.futures
import os
import subprocess


def install_path(path):
    if "MESON_INSTALL_DESTDIR_PREFIX" not in os.environ:
        return os.path.abspath(path)
    if os.path.isabs(path):
        return os.environ.get("DESTDIR", "") + path
    return os.path.join(os.environ["MESON_INSTALL_DESTDIR_PREFIX"], path)


def scan_sources(sources, theme):
    icons = {}
    for context in sorted(os.listdir(sources)):
        for name in sorted(os.listdir(os.path.join(sources, context))):
            svg = os.path.join(theme, "scalable", context, name + ".svg")
            if not os.path.isfile(svg) or os.path.islink(svg):
                raise SystemExit("%s/%s has no SVG next to it" % (context, name))
            icons[os.path.realpath(svg)] = os.path.join(sources, context, name)
    return icons


def scan_aliases(theme, icons):
    aliases = {}
    for dirpath, _, names in os.walk(theme):
        for name in sorted(names):
            path = os.path.join(dirpath, name)
            if name.endswith(".svg") and os.path.islink(path) and os.path.realpath(path) in icons:
                aliases[path] = os.path.realpath(path)
    return aliases


def compiled_path(svg):
    return os.path.splitext(svg)[0] + ".iride"


def build(compiler, source, out):
    result = subprocess.run([compiler, "build", source, out], capture_output=True, text=True)
    if result.returncode:
        raise SystemExit("cannot build %s: %s" % (source, result.stderr.strip()))


def install_aliases(aliases):
    for link, svg in sorted(aliases.items()):
        out = compiled_path(link)
        if os.path.lexists(out):
            os.remove(out)
        os.symlink(os.path.relpath(compiled_path(svg), os.path.realpath(os.path.dirname(link))), out)


def main():
    parser = argparse.ArgumentParser(description="Compile the Iride icons next to their SVG in an installed theme.")
    parser.add_argument("compiler", help="iride compiler")
    parser.add_argument("sources", help="directory of icon sources, by context")
    parser.add_argument("theme", help="installed icon theme directory")
    args = parser.parse_args()
    theme = install_path(args.theme)
    icons = scan_sources(args.sources, theme)
    with concurrent.futures.ThreadPoolExecutor(os.cpu_count()) as pool:
        list(pool.map(lambda item: build(args.compiler, item[1], compiled_path(item[0])), icons.items()))
    install_aliases(scan_aliases(theme, icons))


if __name__ == "__main__":
    main()
