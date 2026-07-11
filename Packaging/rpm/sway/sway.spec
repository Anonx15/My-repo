# RPM spec for sway 1.12
# Build profile: -Dswaybar=false -Dtray=disabled (no swaybar, no tray)
# Linked against wlroots 0.20.0 built without Xwayland and without Vulkan.

Name:           sway
Version:        1.12
Release:        1%{?dist}
Summary:        i3-compatible tiling Wayland compositor
License:        MIT
URL:            https://github.com/swaywm/sway
Source0:        %{url}/archive/%{version}/sway-%{version}.tar.gz

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

# Runtime: wlroots shared library
Requires:       wlroots%{?_isa} >= 0.20.0

# Runtime: GPU drivers (sway cannot start without EGL + GBM + DRI)
Requires:       mesa-dri-drivers%{?_isa}
Requires:       mesa-libEGL%{?_isa}
Requires:       mesa-libgbm%{?_isa}
Requires:       mesa-libGL%{?_isa}

# Recommended: useful but sway runs without them
Recommends:     swaybg
Recommends:     mesa-va-drivers
Recommends:     libva
Recommends:     mesa-vulkan-drivers

%description
Sway is a tiling Wayland compositor and a drop-in replacement for the
i3 window manager. It works with your existing i3 configuration and
supports most of i3's features, plus a few extras.

This build is configured without swaybar and without the system tray.

%prep
%autosetup -n sway-%{version}

%build
%meson \
    -Dwerror=false \
    -Db_lto=true \
    -Db_lto_mode=full \
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
%{_datadir}/bash-completion/completions/sway
%{_datadir}/bash-completion/completions/swaymsg
%{_datadir}/bash-completion/completions/swaynag
%{_datadir}/zsh/site-functions/_sway
%{_datadir}/zsh/site-functions/_swaymsg
%{_datadir}/zsh/site-functions/_swaynag

%changelog
* Fri Jul 11 2026 Builder <builder@localhost> - 1.12-1
- Initial package for sway 1.12
- Built without swaybar and without system tray
- Linked against wlroots 0.20.0 (no Xwayland, no Vulkan)
