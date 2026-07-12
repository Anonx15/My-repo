# sway 1.12 — no swaybar, no tray, no gdk-pixbuf
# Linked against wlroots 0.20.0 (no Xwayland, no Vulkan)

%global toolchain clang
%{!?bdver2_cflags:%global bdver2_cflags -march=bdver2 -mprefer-vector-width=128 -mvzeroupper -fomit-frame-pointer -flto=full}
%{!?bdver2_ldflags:%global bdver2_ldflags -flto=full -fuse-ld=lld -Wl,-O1}
%global build_cflags %{build_cflags} %{bdver2_cflags}
%global build_ldflags %{build_ldflags} %{bdver2_ldflags}

Name:           sway
Version:        1.12
Release:        1%{?dist}
Summary:        i3-compatible tiling Wayland compositor
License:        MIT
URL:            https://github.com/swaywm/sway
Source0:        %{url}/releases/download/%{version}/sway-%{version}.tar.gz

BuildRequires:  meson >= 1.3
BuildRequires:  ninja-build
BuildRequires:  clang
BuildRequires:  lld
BuildRequires:  scdoc
BuildRequires:  pkgconfig(wlroots-0.20) >= 0.20.0
BuildRequires:  pkgconfig(wayland-server) >= 1.21
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.41
BuildRequires:  pkgconfig(xkbcommon) >= 1.5.0
BuildRequires:  pkgconfig(json-c) >= 0.13
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libinput) >= 1.26
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libsystemd) >= 239

Requires:       wlroots%{?_isa} >= 0.20.0
Requires:       mesa-dri-drivers%{?_isa}
Requires:       mesa-libEGL%{?_isa}
Requires:       mesa-libgbm%{?_isa}
Requires:       mesa-libGL%{?_isa}
Recommends:     swaybg
Recommends:     mesa-va-drivers
Recommends:     libva
Recommends:     mesa-vulkan-drivers

%description
Sway is a tiling Wayland compositor and drop-in replacement for i3.
This build has swaybar and tray disabled.

%prep
# Release tarballs extract to sway-%{version}/
%autosetup -n sway-%{version}

%build
%meson \
    -Dwerror=false \
    -Dswaybar=false \
    -Dswaynag=true \
    -Dtray=disabled \
    -Dgdk-pixbuf=disabled \
    -Dman-pages=enabled \
    -Dsd-bus-provider=libsystemd \
    -Ddefault-wallpaper=true \
    -Dbash-completions=true \
    -Dzsh-completions=true \
    -Dfish-completions=false
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_bindir}/sway
%{_bindir}/swaymsg
%{_bindir}/swaynag
%config(noreplace) %{_sysconfdir}/sway/
%{_datadir}/wayland-sessions/sway.desktop
%{_datadir}/backgrounds/sway/
%{_mandir}/man1/sway.1*
%{_mandir}/man1/swaymsg.1*
%{_mandir}/man1/swaynag.1*
%{_mandir}/man5/sway.5*
%{_mandir}/man5/sway-bar.5*
%{_mandir}/man5/sway-input.5*
%{_mandir}/man5/sway-output.5*
%{_mandir}/man5/swaynag.5*
%{_mandir}/man7/sway-ipc.7*
%{_mandir}/man7/swaybar-protocol.7*
%{_datadir}/bash-completion/completions/sway
%{_datadir}/bash-completion/completions/swaymsg
%{_datadir}/zsh/site-functions/_sway
%{_datadir}/zsh/site-functions/_swaymsg

%changelog
* Sun Jul 12 2026 Builder <builder@localhost> - 1.12-1
- sway 1.12 without swaybar/tray
- Built with Clang+LLD full LTO for AMD FX-4320
