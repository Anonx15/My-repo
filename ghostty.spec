Name:           ghostty
Version:        1.3.1
Release:        1.bdver2%{?dist}
Summary:        Fast, native, feature-rich terminal emulator
License:        MIT
URL:            https://ghostty.org

# ──────────────────────────────────────────────────────────
# Runtime dependencies
# ──────────────────────────────────────────────────────────
Requires:       gtk4
Requires:       libadwaita
Requires:       gtk4-layer-shell
Requires:       fontconfig
Requires:       harfbuzz
Requires:       libxkbcommon
Requires:       ncurses


# ──────────────────────────────────────────────────────────
# RPM build macros
# ──────────────────────────────────────────────────────────
%global __os_install_post %{nil}
%global _missing_build_ids_terminate_build 0
%global debug_package %{nil}

# ──────────────────────────────────────────────────────────
%description
Ghostty terminal emulator compiled with ReleaseFast for AMD FX-4320 (bdver2).
Wayland-only build targeting Fedora 44.
Includes full terminfo entries (ghostty + xterm-ghostty) for local ncurses apps.

# ──────────────────────────────────────────────────────────
%install
# ── Binary ────────────────────────────────────────────────
install -Dm755 %{_sourcedir}/output/bin/ghostty \
               %{buildroot}%{_bindir}/ghostty

# ── Desktop entry (GNOME app menu) ────────────────────────
install -Dm644 %{_sourcedir}/output/share/applications/com.mitchellh.ghostty.desktop \
               %{buildroot}%{_datadir}/applications/com.mitchellh.ghostty.desktop

# ── Terminfo: entry "ghostty"  →  g/ghostty ───────────────
install -Dm644 %{_sourcedir}/output/share/terminfo/g/ghostty \
               %{buildroot}%{_datadir}/terminfo/g/ghostty

# ── Terminfo: entry "xterm-ghostty"  →  x/xterm-ghostty ──
#    $TERM ="${xterm-ghostty}" — ncurses looks here first!
install -Dm644 %{_sourcedir}/output/share/terminfo/x/xterm-ghostty \
               %{buildroot}%{_datadir}/terminfo/x/xterm-ghostty

# ── Terminfo source file (needed by tic in %post) ─────────
install -Dm644 %{_sourcedir}/output/share/terminfo/ghostty.terminfo \
               %{buildroot}%{_datadir}/terminfo/ghostty.terminfo

# ── Icons (hicolor + any others) ──────────────────────────
cp -r %{_sourcedir}/output/share/icons \
      %{buildroot}%{_datadir}/

# ── Ghostty resources (shell-integration, themes, etc.) ───
cp -r %{_sourcedir}/output/share/ghostty \
      %{buildroot}%{_datadir}/

# ──────────────────────────────────────────────────────────
%files
%attr(755, root, root) %{_bindir}/ghostty

# Desktop entry → shows Ghostty in GNOME app grid
%{_datadir}/applications/com.mitchellh.ghostty.desktop

# Terminfo binaries (both entries!)
%{_datadir}/terminfo/g/ghostty
%{_datadir}/terminfo/x/xterm-ghostty

# Terminfo source (used by tic on re-install)
%{_datadir}/terminfo/ghostty.terminfo

# Icons & resources
%{_datadir}/icons/
%{_datadir}/ghostty/

# ──────────────────────────────────────────────────────────
%post
# 1) Re-compile terminfo from source to guarantee both entries exist
#    tic -x compiles extended capabilities; -o writes to system db
if [ -f %{_datadir}/terminfo/ghostty.terminfo ]; then
    tic -x -o %{_datadir}/terminfo \
        %{_datadir}/terminfo/ghostty.terminfo 2>/dev/null || true
fi

# 2) Create symlink x/xterm-ghostty → g/ghostty if binary copy missed it
if [ ! -f %{_datadir}/terminfo/x/xterm-ghostty ]; then
    mkdir -p %{_datadir}/terminfo/x
    ln -sf %{_datadir}/terminfo/g/ghostty \
           %{_datadir}/terminfo/x/xterm-ghostty 2>/dev/null || true
fi

# 3) Refresh GNOME / XDG application database → appears in app grid
update-desktop-database %{_datadir}/applications 2>/dev/null || true

# 4) Refresh icon cache
gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor 2>/dev/null || true

# 5) Notify GNOME Shell of new application (if running)
if command -v glib-compile-schemas &>/dev/null; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas 2>/dev/null || true
fi

# ──────────────────────────────────────────────────────────
%postun
update-desktop-database %{_datadir}/applications 2>/dev/null || true
gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor 2>/dev/null || true

# ──────────────────────────────────────────────────────────
%changelog
* Thu Jun 2026 GitHub Actions <actions@github.com> - 1.3.1-3.bdver2
- Compiled with ReleaseFast for AMD FX-4320 (bdver2)
- Wayland-only build on Fedora 44
- freetype statically linked
- Added xterm-ghostty terminfo entry (fixes nano/clear/$TERM issues)
- Added terminfo source file + tic recompile in %%post
- Added fallback symlink x/xterm-ghostty in %%post
- Desktop entry updated for GNOME app grid visibility
