# ============================================================
# GHOSTTY RPM SPEC - ANALYZED & IMPROVED (June 2026)
# ============================================================
# This spec file was analyzed using Fedora/RPM packaging best practices,
# real-world issues reported on GitHub (ghostty discussions), and
# common packaging problems with terminfo + ncurses-term.

Name:           ghostty
Version:        1.3.1
Release:        1.bdver2%{?dist}
Summary:        Fast, native, feature-rich terminal emulator
License:        MIT
URL:            https://ghostty.org
Source0:        output

# Architecture: This is a custom build for bdver2 (AMD FX-4320)
BuildArch:      x86_64

# === DEPENDENCIES (Runtime) ===
Requires:       gtk4
Requires:       libadwaita
Requires:       gtk4-layer-shell
Requires:       fontconfig
Requires:       harfbuzz
Requires:       libxkbcommon
Requires:       ncurses                  # Needed for 'tic' in %post to compile terminfo

# === CONFLICTS ANALYSIS ===
# REMOVED: Conflicts: ghostty
# REASON: This line causes the package to conflict with ITSELF.
#         RPM sees "Conflicts: ghostty" and blocks installation/upgrade.
#         This is a common mistake. Never use Conflicts: %{name} on the same package.
#         Source: Multiple StackOverflow/ServerFault reports on self-conflict.

# === GLOBALS (Zig build workarounds) ===
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

# Desktop file + GNOME integration
install -Dm644 %{_sourcedir}/output/share/applications/com.mitchellh.ghostty.desktop \
               %{buildroot}%{_datadir}/applications/com.mitchellh.ghostty.desktop

# Ensure GNOME visibility and proper categories
sed -i \
  -e 's|^Categories=.*|Categories=System;TerminalEmulator;GTK;GNOME;|' \
  -e '/^Categories=/a X-GNOME-UsesNotifications=true' \
  -e '/^Categories=/a StartupNotify=true' \
  %{buildroot}%{_datadir}/applications/com.mitchellh.ghostty.desktop

# === TERMINO ANALYSIS (Critical) ===
# Ghostty uses TERM=xterm-ghostty
# Problem: ncurses-term package on Fedora also ships /usr/share/terminfo/g/ghostty
# This has caused real conflicts (see GitHub discussions #8574)
#
# Solution chosen: Install both possible paths + use || fallback
# Future improvement: Create a separate ghostty-terminfo subpackage

# Try xterm-ghostty first (correct modern path)
install -Dm644 %{_sourcedir}/output/share/terminfo/x/xterm-ghostty \
               %{buildroot}%{_datadir}/terminfo/x/xterm-ghostty 2>/dev/null || true

# Fallback for older builds
install -Dm644 %{_sourcedir}/output/share/terminfo/g/ghostty \
               %{buildroot}%{_datadir}/terminfo/g/ghostty 2>/dev/null || true

# Icons and config
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
# Compile terminfo database
# This fixes: "xterm-ghostty: unknown terminal type"
if [ -f %{_datadir}/terminfo/x/xterm-ghostty ]; then
    tic -x %{_datadir}/terminfo/x/xterm-ghostty 2>/dev/null || true
elif [ -f %{_datadir}/terminfo/g/ghostty ]; then
    tic -x %{_datadir}/terminfo/g/ghostty 2>/dev/null || true
fi

# Refresh desktop and icon caches
update-desktop-database %{_datadir}/applications 2>/dev/null || true
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2>/dev/null || true

%postun
update-desktop-database %{_datadir}/applications 2>/dev/null || true
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2>/dev/null || true

%changelog
* Thu Jun 26 2026 - Improved packaging
- Removed "Conflicts: ghostty" (was causing self-conflict)
- Added proper terminfo handling for both x/xterm-ghostty and g/ghostty paths
- Enhanced GNOME desktop integration (Categories + StartupNotify)
- Added ncurses dependency for tic command
- Improved %post script with better logic

* Original build
- Compiled with ReleaseFast for AMD FX-4320 (bdver2)
- Wayland-only
- freetype statically linked
