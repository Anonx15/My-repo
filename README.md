# bdver2 — Custom Arch Linux Repository

Personal pacman repository with packages optimized for **AMD FX-4320 (bdver2)**.

## Packages

| Package | Version | Description |
|---------|---------|-------------|
| ghostty | 1.3.1 | Fast, native terminal emulator (Zig ReleaseFast) |
| wlroots | 0.20.0 | Wayland compositor library (Clang+LLD full LTO) |
| sway | 1.12 | i3-compatible Wayland compositor (Clang+LLD full LTO) |

## Usage

Add to `/etc/pacman.conf`:

```ini
[bdver2]
Server = https://<username>.github.io/My-repo/repo/$arch
SigLevel = Optional
```

Then:

```bash
pacman -Syu
pacman -S ghostty sway wlroots
```

## Repository Structure

```
My-repo/
├── .github/workflows/
│   ├── build-ghostty.yml      # Build Ghostty → .pkg.tar.zst
│   ├── build-sway.yml         # Build wlroots + Sway → .pkg.tar.zst
│   └── publish-repo.yml       # Collect packages → repo database
│
├── packages/
│   ├── ghostty/
│   │   ├── PKGBUILD
│   │   └── ghostty.desktop
│   ├── wlroots/
│   │   └── PKGBUILD
│   └── sway/
│       └── PKGBUILD
│
├── repo/x86_64/               # pacman repo (served via GitHub Pages)
│   ├── bdver2.db.tar.gz
│   ├── bdver2.files.tar.gz
│   └── *.pkg.tar.zst
│
├── bdver2.conf                # Example pacman.conf snippet
└── README.md
```

## Build Workflows

Each workflow builds packages in a Fedora 44 container with bdver2-specific flags:

- **build-ghostty.yml** — Builds Ghostty with Zig `ReleaseFast -Dcpu=bdver2`
- **build-sway.yml** — Builds wlroots then Sway with Clang+LLD full LTO and `-march=bdver2`
- **publish-repo.yml** — Downloads build artifacts, runs `repo-add`, pushes to `repo/x86_64/`

## Compiler Flags

All native packages use these bdver2 optimizations:

```
-march=bdver2 -mprefer-vector-width=128 -mvzeroupper
-fomit-frame-pointer -flto=full
```

## Notes

- `.spec` files are kept as reference for PKGBUILD conversion
- Ghostty is built with Zig (not meson/cmake) — see workflow for build steps
- wlroots must be built before Sway (dependency)
