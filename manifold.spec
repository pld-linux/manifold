# This is what openscad@master needs
%define	hash	22c66051dfdbcefa2012e30dd12c9b5a20f89a01
%define	snap	22c6605
Summary:	Geometry library dedicated to creating and operating on manifold triangle meshes
Name:		manifold
Version:	2.5.1
Release:	1.%{snap}.2
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/elalish/manifold/archive/%{snap}/%{name}-%{version}-%{snap}.tar.gz
# Source0-md5:	f88f9a9314a92a6c3fb71c6fc242ae64
Patch0:		install-pkgconfig.patch
Patch1:		install-cmake.patch
Patch2:		sonames.patch
URL:		https://github.com/elalish/manifold
BuildRequires:	Clipper2-devel
BuildRequires:	cmake
BuildRequires:	tbb-devel
# Library may have new symbols without soname change
%requires_eq	tbb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Manifold is a geometry library dedicated to creating and operating on
manifold triangle meshes. A manifold mesh is a mesh that represents a
solid object, and so is very important in manufacturing, CAD,
structural analysis, etc.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -q -n %{name}-%{hash}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
mkdir -p build
cd build
%cmake ../ \
	-DMANIFOLD_PAR=TBB \
	-DMANIFOLD_TEST=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md
%attr(755,root,root) %{_libdir}/libmanifold.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmanifold.so.2
%attr(755,root,root) %{_libdir}/libcross_section.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcross_section.so.2
%attr(755,root,root) %{_libdir}/libpolygon.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpolygon.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmanifold.so
%attr(755,root,root) %{_libdir}/libcross_section.so
%attr(755,root,root) %{_libdir}/libpolygon.so
# C bindings
%attr(755,root,root) %{_libdir}/libmanifoldc.so
%{_includedir}/manifold
%{_libdir}/cmake/manifold
%{_pkgconfigdir}/manifold.pc
