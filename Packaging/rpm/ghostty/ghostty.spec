# Clean, reproducible packaging for Ghostty 1.4.0 on Fedora 45 / KDE Plasma 6.8 (Wayland)

%{!?_userunitdir:%define _userunitdir %{_prefix}/lib/systemd/user}

Name:           ghostty
Version:        1.4.0
Release:        1.bdver2%{?dist}
Summary:        Fast, native, feature-rich terminal emulator
License:        MIT
URL:            https://ghostty.org
Source0:        output

BuildArch:      x86_64

# Runtime dependencies matching Ghostty 1.4.0 requirements on Fedora 45
Requires:       gtk4 >= 4.18
Requires:       libadwaita >= 1.7
Requires:       gtk4-layer-shell >= 1.0.4
Requires:       libglvnd-egl
Requires:       fontconfig
Requires:       libxkbcommon
Requires:       libwayland-client

# Preserve Zig's own ReleaseFast + stripped binary without brp-strip/debuginfo interference
%global __os_install_post %{nil}
%global _missing_build_ids_terminate_build 0
%global debug_package %{nil}

%description
Ghostty terminal emulator compiled with ReleaseFast, PIE (ASLR), and
AMD Piledriver (bdver2) optimization for Fedora 45 KDE Plasma (Wayland-only).

HarfBuzz, FreeType, simdutf, Highway, oniguruma, zlib, and libpng are compiled
statically by Zig targeting bdver2 for lower CPU overhead, while Fontconfig,
GTK4, Adwaita, EGL, Wayland, and Layer Shell link dynamically to system libraries.

%install
# 1. Main executable
install -Dm755 %{_sourcedir}/output/bin/ghostty \
               %{buildroot}%{_bindir}/ghostty

# 2. Desktop entry (generated with -Dinstalled-exe-path=/usr/bin/ghostty; KDE-ready)
install -Dm644 %{_sourcedir}/output/share/applications/com.mitchellh.ghostty.desktop \
               %{buildroot}%{_datadir}/applications/com.mitchellh.ghostty.desktop

# 3. D-Bus activation & systemd user unit (required for single-instance & Plasma launch)
install -Dm644 %{_sourcedir}/output/share/dbus-1/services/com.mitchellh.ghostty.service \
               %{buildroot}%{_datadir}/dbus-1/services/com.mitchellh.ghostty.service

if [ -f %{_sourcedir}/output/share/systemd/user/app-com.mitchellh.ghostty.service ]; then
    install -Dm644 %{_sourcedir}/output/share/systemd/user/app-com.mitchellh.ghostty.service \
                   %{buildroot}%{_userunitdir}/app-com.mitchellh.ghostty.service
elif [ -f %{_sourcedir}/output/lib/systemd/user/app-com.mitchellh.ghostty.service ]; then
    install -Dm644 %{_sourcedir}/output/lib/systemd/user/app-com.mitchellh.ghostty.service \
                   %{buildroot}%{_userunitdir}/app-com.mitchellh.ghostty.service
else
    echo "ERROR: app-com.mitchellh.ghostty.service missing from build output" >&2
    exit 1
fi

# 4. KDE Plasma / Dolphin context menu (KIO) & AppStream metadata
install -Dm644 %{_sourcedir}/output/share/kio/servicemenus/com.mitchellh.ghostty.desktop \
               %{buildroot}%{_datadir}/kio/servicemenus/com.mitchellh.ghostty.desktop

install -Dm644 %{_sourcedir}/output/share/metainfo/com.mitchellh.ghostty.metainfo.xml \
               %{buildroot}%{_datadir}/metainfo/com.mitchellh.ghostty.metainfo.xml

# 5. Terminfo: ship ONLY x/xterm-ghostty.
#    g/ghostty is owned by Fedora's ncurses-term package since F42+.
src_tinfo="%{_sourcedir}/output/share/terminfo/x/xterm-ghostty"
if [ ! -f "${src_tinfo}" ]; then
    echo "ERROR: expected terminfo file missing from build output: ${src_tinfo}" >&2
    exit 1
fi
install -Dm644 "${src_tinfo}" %{buildroot}%{_datadir}/terminfo/x/xterm-ghostty

# 6. Icons and Ghostty runtime resources (themes, shell-integration)
mkdir -p %{buildroot}%{_datadir}
cp -a %{_sourcedir}/output/share/icons %{buildroot}%{_datadir}/icons
cp -a %{_sourcedir}/output/share/ghostty %{buildroot}%{_datadir}/ghostty

# 7. Shell completions
install -Dm644 %{_sourcedir}/output/share/bash-completion/completions/ghostty.bash \
               %{buildroot}%{_datadir}/bash-completion/completions/ghostty.bash
install -Dm644 %{_sourcedir}/output/share/fish/vendor_completions.d/ghostty.fish \
               %{buildroot}%{_datadir}/fish/vendor_completions.d/ghostty.fish
install -Dm644 %{_sourcedir}/output/share/zsh/site-functions/_ghostty \
               %{buildroot}%{_datadir}/zsh/site-functions/_ghostty

# 8. Optional locales (populated only if -Di18n=false is removed)
: > %{_builddir}/ghostty-extra.list
if [ -d %{_sourcedir}/output/share/locale ]; then
    cp -a %{_sourcedir}/output/share/locale %{buildroot}%{_datadir}/locale
    find %{buildroot}%{_datadir}/locale -type f -name "com.mitchellh.ghostty.mo" | \
        sed "s|^%{buildroot}||" >> %{_builddir}/ghostty-extra.list
fi

# Work around upstream 1.4.0 restrictive icon file permissions (#15170)
chmod -R a+rX %{buildroot}%{_datadir}

%files -f %{_builddir}/ghostty-extra.list
%attr(755, root, root) %{_bindir}/ghostty
%{_datadir}/applications/com.mitchellh.ghostty.desktop
%{_datadir}/dbus-1/services/com.mitchellh.ghostty.service
%{_userunitdir}/app-com.mitchellh.ghostty.service
%{_datadir}/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_datadir}/metainfo/com.mitchellh.ghostty.metainfo.xml
%{_datadir}/terminfo/x/xterm-ghostty
%{_datadir}/icons/hicolor/*/apps/com.mitchellh.ghostty.png
%{_datadir}/ghostty/
%{_datadir}/bash-completion/completions/ghostty.bash
%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/zsh/site-functions/_ghostty

%changelog
* Fri Nov 27 2026 - 1.4.0-1.bdver2
- Upgrade to Ghostty 1.4.0 with Zig 0.17.1 on Fedora 45
- Switch to Wayland-only KDE Plasma 6.8 integration (KIO, D-Bus, systemd user unit)
- Build HarfBuzz and FreeType statically with bdver2 tuning
- Add libglvnd-egl runtime dependency for the new EGL renderer
- Drop g/ghostty terminfo to prevent file conflict with Fedora ncurses-term
- Remove invalid tic call on precompiled binary in %%post and fix icon permissions
