# Shared full-LTO compiler/linker flags for Clang+LLD RPM builds.
# Appended to the CFLAGS/LDFLAGS provided by the workflow env / Fedora macros.
# Included inside the %build section of specs using this toolchain.
export CFLAGS="${CFLAGS} -flto=full"
export LDFLAGS="${LDFLAGS} -flto=full"
