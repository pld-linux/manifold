# This is what openscad@master needs
%define	hash	22c66051dfdbcefa2012e30dd12c9b5a20f89a01
%define	snap	22c6605
Summary:	Geometry library dedicated to creating and operating on manifold triangle meshes
Summary(pl.UTF-8):	Biblioteka geometryczna do tworzenia i operacji na siatkach trójkątów rozmaitości
Name:		manifold
Version:	2.5.1
%define	rel	5
Release:	1.%{snap}.%{rel}
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/elalish/manifold/archive/%{snap}/%{name}-%{version}-%{snap}.tar.gz
# Source0-md5:	f88f9a9314a92a6c3fb71c6fc242ae64
Patch0:		install-pkgconfig.patch
Patch1:		install-cmake.patch
Patch2:		sonames.patch
URL:		https://github.com/elalish/manifold
BuildRequires:	Clipper2-devel
BuildRequires:	GLM-devel
BuildRequires:	cmake >= 3.18
# C++17
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	pkgconfig
BuildRequires:	tbb-devel
# Library may have new symbols without soname change
%requires_eq	tbb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Manifold is a geometry library dedicated to creating and operating on
manifold triangle meshes. A manifold mesh is a mesh that represents a
solid object, and so is very important in manufacturing, CAD,
structural analysis, etc.

%description -l pl.UTF-8
Manifold to bibliotek geometryczna przeznaczona do tworzenia oraz
operacji na siatkach trójkątów rozmaitości geometrycznych. Siatka
rozmaitości to siatka reprezentująca bryłę, przez co jest istotna w
dziedzinach produkcji, CAD, analizy strukturalnej itp.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Clipper2-devel
Requires:	GLM-devel
Requires:	libstdc++-devel >= 6:7
Requires:	pkgconfig
Requires:	tbb-devel

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -q -n %{name}-%{hash}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
%cmake -B build \
	-DMANIFOLD_PAR=TBB \
	-DMANIFOLD_TEST=OFF

%{__make} -C build

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
# C bindings
%attr(755,root,root) %{_libdir}/libmanifoldc.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmanifold.so
%attr(755,root,root) %{_libdir}/libcross_section.so
%attr(755,root,root) %{_libdir}/libpolygon.so
%{_includedir}/manifold
%{_libdir}/cmake/manifold
%{_pkgconfigdir}/manifold.pc
