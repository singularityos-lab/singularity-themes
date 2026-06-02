project('singularity-themes', version: '0.1.0', meson_version: '>= 0.59.0')

# GTK theme (empty CSS, applied per-process for theme isolation).
install_subdir('themes/Singularity',
  install_dir: get_option('datadir') / 'themes',
  strip_directory: false)

# Icon theme.
install_subdir('Singularity-Material',
  install_dir: get_option('datadir') / 'icons',
  strip_directory: false)
