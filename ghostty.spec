Name:           ghostty
Version:        1.3.1
Release:        1.bdver2%{?dist}
Summary:        Fast, native, feature-rich terminal emulator
License:        MIT
URL:            https://ghostty.org

Requires:       gtk4
Requires:       libadwaita
Requires:       gtk4-layer-shell
Requires:       fontconfig
Requires:       harfbuzz
Requires:       libxkbcommon
Requires:       wayland-libs-client

Conflicts:      ghostty

%global __os_install_post %{nil}
%global _missing_build_ids_terminate_build 0
%global debug_package %{nil}

%description
Ghostty terminal emulator compiled with ReleaseFast for AMD FX-4320 (bdver2).
Wayland-only build targeting Sway WM on Fedora 44.

%install
install -Dm755 %{_sourcedir}/output/bin/ghostty \
               %{buildroot}/usr/bin/ghostty

install -Dm644 %{_sourcedir}/output/share/applications/com.mitchellh.ghostty.desktop \
               %{buildroot}/usr/share/applications/com.mitchellh.ghostty.desktop

install -Dm644 %{_sourcedir}/output/share/terminfo/g/ghostty \
               %{buildroot}/usr/share/terminfo/g/ghostty

cp -r %{_sourcedir}/output/share/icons \
      %{buildroot}/usr/share/icons

cp -r %{_sourcedir}/output/share/ghostty \
      %{buildroot}/usr/share/ghostty

find %{_sourcedir}/output/share/man -type f -name "*.1" -exec \
    install -Dm644 {} %{buildroot}/usr/share/man/man1/{} \; 2>/dev/null || true

find %{_sourcedir}/output/share/man -type f -name "*.5" -exec \
    install -Dm644 {} %{buildroot}/usr/share/man/man5/{} \; 2>/dev/null || true

%files
%attr(755, root, root) /usr/bin/ghostty
/usr/share/applications/com.mitchellh.ghostty.desktop
/usr/share/terminfo/g/ghostty
/usr/share/icons/
/usr/share/ghostty/
%optional /usr/share/man/man1/ghostty.1
%optional /usr/share/man/man5/ghostty.5

%post
tic -x /usr/share/terminfo/g/ghostty 2>/dev/null || true
update-desktop-database /usr/share/applications 2>/dev/null || true
gtk-update-icon-cache /usr/share/icons/hicolor 2>/dev/null || true

%postun
update-desktop-database /usr/share/applications 2>/dev/null || true
gtk-update-icon-cache /usr/share/icons/hicolor 2>/dev/null || true

%changelog
* Thu May 15 2025 GitHub Actions <actions@github.com> - 1.3.1-1
- ReleaseFast build for AMD FX-4320 (bdver2)
- Wayland-only
- Font backend: fontconfig_freetype
- Renderer: OpenGL
