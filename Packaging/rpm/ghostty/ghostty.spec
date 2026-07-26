# Clean, maintainable packaging for custom Ghostty builds

Name:           ghostty
Version:        1.3.1
Release:        1.bdver2%{?dist}
Summary:        Fast, native, feature-rich terminal emulator
License:        MIT
URL:            https://ghostty.org
Source0:        output

BuildArch:      x86_64

Requires:       gtk4
Requires:       libadwaita
Requires:       gtk4-layer-shell
Requires:       fontconfig
Requires:       harfbuzz
Requires:       libxkbcommon
Requires:       ncurses

%global __os_install_post %{nil}
%global _missing_build_ids_terminate_build 0
%global debug_package %{nil}

%description
Ghostty terminal emulator compiled with ReleaseFast for AMD FX-4320 (bdver2).

Wayland-only build targeting Sway WM on Fedora 44.
Fast, GPU-accelerated terminal with excellent Wayland support.

%install
# Binary
install -Dm755 %{_sourcedir}/output/bin/ghostty \
               %{buildroot}%{_bindir}/ghostty

# Custom desktop file (Sway + Wayland compatible)
install -Dm644 %{_sourcedir}/com.mitchellh.ghostty.desktop \
               %{buildroot}%{_datadir}/applications/com.mitchellh.ghostty.desktop

# Terminfo installation
# These were previously installed with `2>/dev/null || true`, which hid any
# failure here only for the build to fail later with a confusing "file not
# found" from %files (which lists both paths as mandatory). Fail loudly and
# early instead, with a message that says what is actually missing.
for tinfo in x/xterm-ghostty g/ghostty; do
    src="%{_sourcedir}/output/share/terminfo/${tinfo}"
    if [ ! -f "${src}" ]; then
        echo "ERROR: expected terminfo file missing from build output: ${src}" >&2
        exit 1
    fi
    install -Dm644 "${src}" "%{buildroot}%{_datadir}/terminfo/${tinfo}"
done

# Icons and resources
cp -r %{_sourcedir}/output/share/icons \
      %{buildroot}%{_datadir}/icons

cp -r %{_sourcedir}/output/share/ghostty \
      %{buildroot}%{_datadir}/ghostty

%files
%attr(755, root, root) %{_bindir}/ghostty
%{_datadir}/applications/com.mitchellh.ghostty.desktop
%{_datadir}/terminfo/x/xterm-ghostty
%{_datadir}/terminfo/g/ghostty
# Only claim this package's own icon files, not the shared
# datadir icons tree (owned by the filesystem/hicolor packages).
%{_datadir}/icons/hicolor/*/apps/com.mitchellh.ghostty.png
%{_datadir}/ghostty/

%post
# Compile terminfo database (fixes "xterm-ghostty: unknown terminal type")
if [ -f %{_datadir}/terminfo/x/xterm-ghostty ]; then
    tic -x %{_datadir}/terminfo/x/xterm-ghostty 2>/dev/null || true
elif [ -f %{_datadir}/terminfo/g/ghostty ]; then
    tic -x %{_datadir}/terminfo/g/ghostty 2>/dev/null || true
fi

update-desktop-database %{_datadir}/applications 2>/dev/null || true
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2>/dev/null || true

%postun
update-desktop-database %{_datadir}/applications 2>/dev/null || true
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2>/dev/null || true

%changelog
* Thu Jul 22 2026 - Professional clean version
- Fixed _missing_build_ids_terminate_build typo
- Made terminfo installation robust with fallback
- Updated desktop file for Sway/Wayland compatibility
- Removed GNOME-only restrictions
- Proper ncurses dependency for tic

* Original build
- Compiled with ReleaseFast for AMD FX-4320 (bdver2)
- Wayland-only
- freetype statically link
