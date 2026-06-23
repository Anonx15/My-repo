# Wraps the pre-built output tree produced by the build workflow.
# The big change vs the previous spec: we install the terminfo entry
# under BOTH g/ghostty AND x/xterm-ghostty so ncurses can resolve the
# TERM value that Ghostty itself exports at runtime.

# Skip the default find-requires / strip post steps: the zig build already
# strips and statically links some libs, which confuses the auto-detectors.
%global __os_install_post %{nil}
%global _missing_build_ids_terminate_build 0
%global debug_package %{nil}
%global __strip %{nil}

Name:           ghostty
Version:        1.3.1
Release:        1.bdver2%{?dist}
Summary:        Fast, native, feature-rich terminal emulator
License:        MIT
URL:            https://ghostty.org

# Build deps kept for documentation. This package wraps a pre-built output
# tree, but listing them here is good practice if someone ever wants to
# rebuild from a source RPM.
BuildRequires:  rpmdevtools
BuildRequires:  ncurses-devel
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  gtk4-layer-shell-devel
BuildRequires:  fontconfig-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  pkgconf-pkg-config

# Runtime deps
Requires:       gtk4
Requires:       libadwaita
Requires:       gtk4-layer-shell
Requires:       fontconfig
Requires:       harfbuzz
Requires:       libxkbcommon
Requires:       ncurses
Requires:       glib2

# Virtual provides so other packages can `Requires: terminfo(ghostty)`.
# Matches what ncurses upstream does for its own terminfo entries.
Provides:       terminfo(ghostty)
Provides:       terminfo(xterm-ghostty)

# NOTE: previous spec had "Conflicts: ghostty" which conflicts with itself
# and broke reinstalls. Removed.

%description
Ghostty is a fast, native, feature-rich, and cross-platform terminal
emulator built with Zig and GTK 4. It uses platform-native UI and
GPU acceleration.

This package was compiled with ReleaseFast targeting AMD FX-4320
(bdver2), Wayland-only, with freetype statically linked. Built for
Sway WM on Fedora 44.

%install
# --- Binary ---------------------------------------------------------------
install -Dm755 %{_sourcedir}/output/bin/ghostty \
               %{buildroot}%{_bindir}/ghostty

# --- Desktop entry --------------------------------------------------------
install -Dm644 %{_sourcedir}/output/share/applications/com.mitchellh.ghostty.desktop \
               %{buildroot}%{_datadir}/applications/com.mitchellh.ghostty.desktop

# --- Terminfo -------------------------------------------------------------
# The zig build places the compiled terminfo at one of these depending on
# the Ghostty version:
#   output/share/terminfo/x/xterm-ghostty   (most builds, named xterm-ghostty)
#   output/share/terminfo/g/ghostty        (some older / alt configs)
# We need BOTH paths populated in the final RPM because:
#   * Ghostty exports TERM=xterm-ghostty at runtime
#   * A few shells/tools probe for TERM=ghostty too
mkdir -p %{buildroot}%{_datadir}/terminfo/g
mkdir -p %{buildroot}%{_datadir}/terminfo/x

TI_SRC=""
for cand in \
    %{_sourcedir}/output/share/terminfo/x/xterm-ghostty \
    %{_sourcedir}/output/share/terminfo/g/ghostty ; do
    if [ -f "$cand" ]; then
        TI_SRC="$cand"
        break
    fi
done

if [ -z "$TI_SRC" ]; then
    echo "ERROR: ghostty terminfo not found in build output" >&2
    echo "Looked for:" >&2
    echo "  %{_sourcedir}/output/share/terminfo/x/xterm-ghostty" >&2
    echo "  %{_sourcedir}/output/share/terminfo/g/ghostty" >&2
    exit 1
fi

# Ship the file at both locations. ncurses finds by path, not by internal
# header name, so this is sufficient. The %post scriptlet below also has a
# self-heal step that recompiles from source if anyone strips the file.
install -Dm644 "$TI_SRC" %{buildroot}%{_datadir}/terminfo/g/ghostty
install -Dm644 "$TI_SRC" %{buildroot}%{_datadir}/terminfo/x/xterm-ghostty

# --- Icons ----------------------------------------------------------------
# Install hicolor icons properly so GNOME's app grid picks them up.
# `cp -a` does NOT create parent directories, so we must mkdir first.
if [ -d %{_sourcedir}/output/share/icons/hicolor ]; then
    install -d %{buildroot}%{_datadir}/icons
    cp -a %{_sourcedir}/output/share/icons/hicolor/. \
          %{buildroot}%{_datadir}/icons/hicolor/
fi

# --- Share data (config, lib, theme, etc.) --------------------------------
if [ -d %{_sourcedir}/output/share/ghostty ]; then
    install -d %{buildroot}%{_datadir}/ghostty
    cp -a %{_sourcedir}/output/share/ghostty/. \
          %{buildroot}%{_datadir}/ghostty/
fi

# --- Man page (if produced) -----------------------------------------------
if [ -f %{_sourcedir}/output/share/man/man1/ghostty.1 ]; then
    install -Dm644 %{_sourcedir}/output/share/man/man1/ghostty.1 \
                   %{buildroot}%{_mandir}/man1/ghostty.1
fi

# --- Locale / translations (if produced) ----------------------------------
if [ -d %{_sourcedir}/output/share/locale ]; then
    install -d %{buildroot}%{_datadir}/locale
    cp -a %{_sourcedir}/output/share/locale/. \
          %{buildroot}%{_datadir}/locale/
fi

%files
%attr(755, root, root) %{_bindir}/ghostty
%{_datadir}/applications/com.mitchellh.ghostty.desktop
%{_datadir}/terminfo/g/ghostty
%{_datadir}/terminfo/x/xterm-ghostty
%{_datadir}/icons/hicolor/*/apps/com.mitchellh.ghostty*
%{_datadir}/ghostty/*
%{_mandir}/man1/ghostty.1*
%{_datadir}/locale/*/LC_MESSAGES/ghostty.mo

%post
# Self-heal: if xterm-ghostty terminfo is missing (stripped by another pkg,
# manual rm, etc.) recreate it from the ghostty entry. We decompile with
# infocmp, rename, and recompile with tic so the embedded header name
# matches the path. Errors here are non-fatal.
if [ ! -f %{_datadir}/terminfo/x/xterm-ghostty ] && [ -f %{_datadir}/terminfo/g/ghostty ]; then
    TMP_TI=$(mktemp)
    if TERMINFO=%{_datadir}/terminfo infocmp -A ghostty > "$TMP_TI" 2>/dev/null; then
        # First line of terminfo source is "name|description,"
        sed -i '1s/^ghostty[|,]/xterm-ghostty|,/' "$TMP_TI"
        TERMINFO=%{_datadir}/terminfo tic -x "$TMP_TI" 2>/dev/null || true
    fi
    rm -f "$TMP_TI"
fi

# Refresh desktop / icon caches so Ghostty shows up in GNOME's app grid
# (Settings > Applications, the GNOME Shell app picker, the dock, etc.)
update-desktop-database %{_datadir}/applications 2>/dev/null || true
if command -v gtk4-update-icon-cache >/dev/null 2>&1; then
    gtk4-update-icon-cache -f -t %{_datadir}/icons/hicolor 2>/dev/null || true
else
    gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor 2>/dev/null || true
fi

%postun
update-desktop-database %{_datadir}/applications 2>/dev/null || true
if command -v gtk4-update-icon-cache >/dev/null 2>&1; then
    gtk4-update-icon-cache -f -t %{_datadir}/icons/hicolor 2>/dev/null || true
else
    gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor 2>/dev/null || true
fi

%changelog
* Mon Jun 22 2026 GitHub Actions <actions@github.com> - 1.3.1-1.bdver2
- Compiled with ReleaseFast for AMD FX-4320 (bdver2)
- Wayland-only
- freetype statically linked
- Install terminfo under BOTH g/ghostty and x/xterm-ghostty so ncurses
  can resolve TERM=xterm-ghostty inside a running Ghostty session
- Add Provides: terminfo(ghostty) and terminfo(xterm-ghostty)
- Self-heal xterm-ghostty at install time via infocmp + tic if missing
- Refresh desktop + icon caches in %post so the entry appears in GNOME
- Drop erroneous "Conflicts: ghostty" self-conflict
- Add BuildRequires/Requires for completeness
- Install man page and locale files when present
- Use install -Dm644 for icons with wildcards in %files for clean ownership
