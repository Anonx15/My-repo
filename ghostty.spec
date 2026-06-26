# ============================================================
# GHOSTTY RPM SPEC - CORRECTED (June 2026)
# ============================================================

Name:           ghostty
Version:        1.3.1
Release:        1.bdver2%{?dist}
Summary:        Fast, native, feature-rich terminal emulator
License:        MIT
URL:            https://ghostty.org
Source0:        output

BuildArch:      x86_64

# Runtime dependencies
Requires:       gtk4
Requires:       libadwaita
Requires:       gtk4-layer-shell
Requires:       fontconfig
Requires:       harfbuzz
Requires:       libxkbcommon
Requires:       ncurses

# ncurses is required because %post uses the 'tic' command
# to compile the terminfo entry for xterm-ghostty

%global __os_install_post %{nil}
%global _missing_build_ids_terminate_build 0
%global debug_package %{nil}

%description
Ghostty terminal emulator compiled with ReleaseFast for AMD FX-4320 (bdver2).

Wayland-only build targeting Sway WM on Fedora 44.
Fast, GPU-accelerated terminal with excellent Wayland support.

%install
install -Dm755 %{_sourcedir}/output/bin/ghostty \
               %{buildroot}%{_bindir}/ghostty

install -Dm644 %{_sourcedir}/output/share/applications/com.mitchellh.ghostty.desktop \
               %{buildroot}%{_datadir}/applications/com.mitchellh.ghostty.desktop

# Add GNOME-specific categories
sed -i \
  -e 's|^Categories=.*|Categories=System;TerminalEmulator;GTK;GNOME;|' \
  -e '/^Categories=/a X-GNOME-UsesNotifications=true' \
  -e '/^Categories=/a StartupNotify=true' \
  %{buildroot}%{_datadir}/applications/com.mitchellh.ghostty.desktop

# Install terminfo (xterm-ghostty support)
install -Dm644 %{_sourcedir}/output/share/terminfo/x/xterm-ghostty \
               %{buildroot}%{_datadir}/terminfo/x/xterm-ghostty 2>/dev/null || true

install -Dm644 %{_sourcedir}/output/share/terminfo/g/ghostty \
               %{buildroot}%{_datadir}/terminfo/g/ghostty 2>/dev/null || true

cp -r %{_sourcedir}/output/share/icons \
      %{buildroot}%{_datadir}/icons

cp -r %{_sourcedir}/output/share/ghostty \
      %{buildroot}%{_datadir}/ghostty

%files
%attr(755, root, root) %{_bindir}/ghostty
%{_datadir}/applications/com.mitchellh.ghostty.desktop
%{_datadir}/terminfo/x/xterm-ghostty
%{_datadir}/terminfo/g/ghostty
%{_datadir}/icons/
%{_datadir}/ghostty/

%post
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
* Thu Jun 26 2026 - Fixed RPM parsing error
- Removed inline comments from Requires lines
- All previous fixes preserved
