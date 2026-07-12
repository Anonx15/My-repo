# wlroots 0.20.0 — DRM+libinput backends, GLES2 renderer only
# No Xwayland, no X11 backend, no Vulkan renderer

%global toolchain clang
%global wlroots_soname 0.20
%{!?bdver2_cflags:%global bdver2_cflags -march=bdver2 -mprefer-vector-width=128 -mvzeroupper -fomit-frame-pointer -flto=full}
%{!?bdver2_ldflags:%global bdver2_ldflags -flto=full -fuse-ld=lld -Wl,-O1}
%global build_cflags %{build_cflags} %{bdver2_cflags}
%global build_ldflags %{build_ldflags} %{bdver2_ldflags}

Name:           wlroots
Version:        0.20.0
Release:        1%{?dist}
Summary:        Modular Wayland compositor library
License:        MIT
URL:            https://gitlab.freedesktop.org/wlroots/wlroots
Source0:        %{url}/-/releases/%{version}/downloads/wlroots-%{version}.tar.gz

BuildRequires:  meson >= 0.59
BuildRequires:  ninja-build
BuildRequires:  clang
BuildRequires:  lld
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
BuildRequires:  pkgconfig(lcms2)
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
# Release tarballs extract to wlroots-%{version}/
%autosetup -n wlroots-%{version}

%build
# %{build_cflags} = Fedora's base flags (-O2, -g, hardening, etc.)
# We append bdver2-specific flags on top.
# -march=bdver2              : Piledriver instruction scheduling + ISA
# -mprefer-vector-width=128  : avoid 256-bit AVX (Piledriver penalty)
# -mvzeroupper               : clean AVX→SSE transitions
# -fomit-frame-pointer       : reclaim RBP register (16 GPRs are scarce)
# -flto=full                 : monolithic LTO for max cross-module optimization
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
%{_libdir}/libwlroots-%{wlroots_soname}.so

%files devel
%{_includedir}/wlroots-%{wlroots_soname}/
%{_libdir}/pkgconfig/wlroots-%{wlroots_soname}.pc

%changelog
* Sun Jul 12 2026 Builder <builder@localhost> - 0.20.0-1
- wlroots 0.20.0 with DRM+libinput, GLES2 renderer
- Built with Clang+LLD full LTO for AMD FX-4320
