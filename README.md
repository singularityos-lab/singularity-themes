# Singularity Themes

> [!IMPORTANT]
> Report bugs and request features in the
> [Singularity Desktop tracker](https://github.com/singularityos-lab/singularity-desktop/issues/new/choose).

GTK and icon themes for the Singularity Desktop Environment.

- `themes/Singularity` - the default GTK theme (installed to `share/themes/`)
- `themes/Kids` - a playful theme, installed by default (`share/themes/`)
- `Singularity` - the icon theme (installed to `share/icons/`, inherits Adwaita)
- `themes/SingularityExample` - a reference theme for authors, not installed

## Build & Install

```sh
meson setup build
meson install -C build
```

## License

GPL-3.0-only - see [LICENSE](LICENSE).

## Use of Generative AI

Maintainers may use generative AI tools as assistants while working on singularity-themes. Non-trivial assisted commits disclose the tool, model, and scope of the work.

AI tools may assist with code comments, documentation, repetitive code, and issue triage. Maintainers make project decisions and review every assisted change before it is merged.

Use these trailers for non-trivial assisted commits:

```plain
Assisted-by: <tool>:<model-version>
AI-Scope: <what the tool generated and the prompt or a short prompt summary>
```

Single-line completions, renames, and formatting changes do not need trailers.

Coding agents must also follow [AGENTS.md](AGENTS.md) before changing files,
creating commits, or opening pull requests.
