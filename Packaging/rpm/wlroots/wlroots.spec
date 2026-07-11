# RPM spec for wlroots 0.20.0
# Build profile: -Dxwayland=disabled -Dbackends=drm,libinput -Drenderers=gles2

%global wlroots_soname 0.20

Name:           wlroots
Version:        0.20.0
Release:        1%{?dist}
Summary:        Modular Wayland compositor library
License:        MIT
URL:            https://gitlab.freedesktop.org/wlroots/wlroots
Source0:        %{url}/-/archive/%{version}/wlroots-%{version}.tar.gz

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
BuildRequires:  hwdata-devel

# Runtime Requires are auto-detected by RPM from the linked .so files.
# No explicit Requires needed.

%description
A modular Wayland compositor library used by sway and other
wlroots-based compositors.

This build provides the DRM and libinput backends with the GLES2
renderer. Xwayland, the X11 backend, and the Vulkan renderer are
disabled.

%package        devel
Summary:        Development files for wlroots
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Headers and pkg-config file needed to build compositors
against libwlroots.

%prep
%autosetup -n wlroots-%{version}

%build
%meson \
    -Dwerror=false \
    -Db_lto=true \
    -Db_lto_mode=full \
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
* Fri Jul 11 2026 Builder <builder@localhost> - 0.20.0-1
- Initial package for wlroots 0.20.0
- DRM + libinput backends, GLES2 renderer only
- Xwayland, X11 backend, and Vulkan renderer disabled
