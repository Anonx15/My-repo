Name:           ghostty
Version:        1.3.1
Release:        1.bdver2%{?dist}
Summary:        Fast, native, feature-rich terminal emulator
License:        MIT
URL:            https://ghostty.org


%global __os_install_post %{nil}
%global _missing_build_ids_terminate_build 0
%global debug_package %{nil}


Requires:       gtk4
Requires:       libadwaita
Requires:       libxkbcommon
Requires:       hicolor-icon-theme


%description
Ghostty terminal emulator compiled with ReleaseFast for AMD FX-4320 (bdver2).
Wayland-only build targeting Sway WM on Fedora. 
freetype, harfbuzz, and gtk4-layer-shell are statically linked.


%install

install -Dpm755 %{_sourcedir}/output/bin/ghostty \
               %{buildroot}%{_bindir}/ghostty

install -Dpm644 %{_sourcedir}/output/share/applications/com.mitchellh.ghostty.desktop \
               %{buildroot}%{_datadir}/applications/com.mitchellh.ghostty.desktop

install -Dpm644 %{_sourcedir}/output/share/terminfo/g/ghostty \
               %{buildroot}%{_datadir}/terminfo/g/ghostty


cp -r %{_sourcedir}/output/share/icons %{buildroot}%{_datadir}/
cp -r %{_sourcedir}/output/share/ghostty %{buildroot}%{_datadir}/

%files
%{_bindir}/ghostty
%{_datadir}/applications/com.mitchellh.ghostty.desktop
%{_datadir}/terminfo/g/ghostty

%dir %{_datadir}/ghostty
%{_datadir}/ghostty/*

%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg

%post

update-desktop-database &>/dev/null || :
gtk-update-icon-cache -f &>/dev/null || :

%postun

update-desktop-database &>/dev/null || :
gtk-update-icon-cache -f &>/dev/null || :

%changelog
* Thu Jun 20 2026 GitHub Actions <actions@github.com> - 1.3.1-2
- Compiled with ReleaseFast for AMD FX-4320 (bdver2)- Wayland-only
- freetype statically linked
