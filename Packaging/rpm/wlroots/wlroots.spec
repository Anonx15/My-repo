# wlroots 0.20.0 — DRM+libinput backends, GLES2 renderer only
# No Xwayland, no X11 backend, no Vulkan renderer

%global wlroots_soname 0.20

Name:           wlroots
Version:        0.20.0
Release:        1%{?dist}
Summary:        Modular Wayland compositor library
License:        MIT
URL:            https://gitlab.freedesktop.org/wlroots/wlroots
Source0:        %{url}/-/archive/%{version}/wlroots-%{version}.tar.gz

BuildRequires:  meson >= 0.59
%include Packaging/rpm/common/toolchain-buildrequires.inc
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-server) >= 1.22
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.35
BuildRequires:  pkgconfig(xkbcommon) >= 1.5.0
BuildRequires:  pkgconfig(libdrm) >= 2.4.114
BuildRequires:  pkgconfig(gbm) >= 17.1.0
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libinput) >= 1.21
BuildRequires:  pkgconfig(libseat) >= 0.2
BuildRequires:  pkgconfig(libdisplay-info) >= 0.1
BuildRequires:  pkgconfig(libliftoff) >= 0.4
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  hwdata-devel

%description
A modular Wayland compositor library used by sway and other
wlroots-based compositors. This build provides DRM and libinput
backends with the GLES2 renderer.

%package        devel
Summary:        Development files for wlroots
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Headers and pkg-config file for building against libwlroots.

%prep
%autosetup -n wlroots-%{version}

%build
%include Packaging/rpm/common/lto-build-flags.inc

%meson \
    -Dwerror=false \
    -Dexamples=false \
    -Dxwayland=disabled \
    -Drenderers=gles2 \
    -Dbackends=drm,libinput
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libwlroots-%{wlroots_soname}.so.*

%files devel
%{_includedir}/wlr/
%{_libdir}/libwlroots-%{wlroots_soname}.so
%{_libdir}/pkgconfig/wlroots-%{wlroots_soname}.pc

%changelog
* Sat Jul 12 2026 Builder <builder@localhost> - 0.20.0-1
- wlroots 0.20.0 with DRM+libinput, GLES2 renderer
- Built with Clang+LLD full LTO for AMD FX-4320
