%define sover 0.11
%define api 1.0
%define libname %mklibname uv %{sover}
%define devname %mklibname -d uv

Name:		libuv
Version:	0.11.21
Release:	1
Summary:	Platform layer for node.js

Group:		Development/Other
# the licensing breakdown is described in detail in the LICENSE file
License:	MIT and BSD and ISC
URL:		http://nodejs.org/
Source0:	http://libuv.org/dist/v%{version}/%{name}-v%{version}.tar.gz
Source2:	libuv.pc.in

BuildRequires: gyp

%description
libuv is a new platform layer for Node. Its purpose is to abstract IOCP on
Windows and libev on Unix systems. We intend to eventually contain all platform
differences in this library.


%package -n %{libname}
Summary:    %{summary}
Group:      System/Libraries

%description -n %{libname}
%{summary}

%package -n	%{devname}
Summary:	Development libraries for libuv
Group:		Development/C
Requires: %{libname} = %{version}-%{release}

%description -n %{devname}
Development libraries for libuv

%prep
%setup -q -n %{name}-v%{version}

%build
echo "m4_define([UV_EXTRA_AUTOMAKE_FLAGS], [serial-tests])" \
        > m4/libuv-extra-automake-flags.m4
libtoolize --install --copy --force --automake
aclocal -I m4
autoconf
automake --add-missing --copy --foreign

export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'
%configure2_5x

%make

%install
%makeinstall_std
# Create the pkgconfig file
mkdir -p %{buildroot}/%{_libdir}/pkgconfig

sed -e "s#@prefix@#%{_prefix}#g" \
    -e "s#@exec_prefix@#%{_exec_prefix}#g" \
    -e "s#@libdir@#%{_libdir}#g" \
    -e "s#@includedir@#%{_includedir}#g" \
    -e "s#@version@#%{version}#g" \
    %SOURCE2 > %{buildroot}/%{_libdir}/pkgconfig/libuv.pc

%check
# Tests are currently disabled because some require network access
# Working with upstream to split these out
#./run-tests
#./run-benchmarks

%files -n %{libname}
%{_libdir}/libuv.so.*

%files -n %{devname}
%doc README.md AUTHORS LICENSE
%{_libdir}/libuv.so
%{_libdir}/pkgconfig/libuv.pc
%{_includedir}/uv*.h
