project('singularity-themes', version: '0.1.0', meson_version: '>= 0.59.0')

python = import('python').find_installation('python3')

install_subdir('themes/SingularityShell',
  install_dir: get_option('datadir') / 'themes',
  strip_directory: false)

install_subdir('themes/Kids',
  install_dir: get_option('datadir') / 'themes',
  strip_directory: false)

if meson.version().version_compare('>= 1.3.0')
  install_subdir('Singularity',
    install_dir: get_option('datadir') / 'icons',
    strip_directory: false,
    follow_symlinks: false)
else
  install_subdir('Singularity',
    install_dir: get_option('datadir') / 'icons',
    strip_directory: false)
endif

if meson.version().version_compare('>= 1.3.0')
  install_subdir('cursors/Singularity/cursors',
    install_dir: get_option('datadir') / 'icons' / 'Singularity',
    follow_symlinks: false)
else
  install_subdir('cursors/Singularity/cursors',
    install_dir: get_option('datadir') / 'icons' / 'Singularity')
endif

meson.add_install_script(python, meson.current_source_dir() / 'tools' / 'accent-icons.py',
  meson.current_source_dir() / 'Singularity',
  get_option('datadir') / 'icons')
