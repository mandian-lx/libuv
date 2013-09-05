%define sover 0.10
%define api 1.0
%define libname %mklibname uv %{sover}
%define devname %mklibname -d uv

Name:		libuv
Version:	0.10.14
Release:	1
Summary:	Platform layer for node.js

Group:		Development/Other
# the licensing breakdown is described in detail in the LICENSE file
License:	MIT and BSD and ISC
URL:		http://nodejs.org/
Source0:	http://libuv.org/dist/v%{version}/%{name}-v%{version}.tar.gz
Source2:	libuv.pc.in

#BuildRequires: gyp

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
export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'
./gyp_uv -Dcomponent=shared_library -Dlibrary=shared_library

%make V=1 -C out BUILDTYPE=Release

%install
# Copy the shared lib into the libdir
mkdir -p %{buildroot}/%{_libdir}/
cp out/Release/obj.target/libuv.so %{buildroot}/%{_libdir}/libuv.so.%{sover}
pushd %{buildroot}/%{_libdir}/
ln -s libuv.so.%{sover} libuv.so.0
ln -s libuv.so.%{sover} libuv.so
popd

# Copy the headers into the include path
mkdir -p %{buildroot}/%{_includedir}/uv-private

cp include/uv.h \
   %{buildroot}/%{_includedir}

cp \
   include/uv-private/ngx-queue.h \
   include/uv-private/tree.h \
   include/uv-private/uv-linux.h \
   include/uv-private/uv-unix.h \
   %{buildroot}/%{_includedir}/uv-private

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
%{_includedir}/uv.h
%{_includedir}/uv-private
