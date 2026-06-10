# Singularity Themes

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
