#
# Conditional build:
%bcond_without	python		# Python (nanobind) binding

Summary:	Geometry library dedicated to creating and operating on manifold triangle meshes
Summary(pl.UTF-8):	Biblioteka geometryczna do tworzenia i operacji na siatkach trójkątów rozmaitości
Name:		manifold
Version:	3.5.4
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/elalish/manifold/releases
Source0:	https://github.com/elalish/manifold/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d12566a37f70d265bd566c743433d5b7
URL:		https://github.com/elalish/manifold
BuildRequires:	Clipper2-devel
BuildRequires:	cmake >= 3.18
# C++17
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	pkgconfig
%if %{with python}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-nanobind
%endif
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
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	Clipper2-devel
Requires:	libstdc++-devel >= 6:7
Requires:	tbb-devel

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package -n python3-manifold
Summary:	Python binding for manifold library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki manifold
Group:		Libraries/Python
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python3-numpy

%description -n python3-manifold
Python binding for manifold library.

%description -n python3-manifold -l pl.UTF-8
Wiązanie Pythona do biblioteki manifold.

%prep
%setup -q

%build
%cmake -B build \
	-DMANIFOLD_DOWNLOAD=OFF \
	-DMANIFOLD_PAR=TBB \
	%{?with_python:-DMANIFOLD_PYBIND=ON} \
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
%{_libdir}/libmanifold.so.*.*.*
%ghost %{_libdir}/libmanifold.so.3
# C bindings
%{_libdir}/libmanifoldc.so.*.*.*
%ghost %{_libdir}/libmanifoldc.so.3

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmanifold.so
%{_libdir}/libmanifoldc.so
%{_includedir}/manifold
%{_libdir}/cmake/manifold
%{_pkgconfigdir}/manifold.pc

%if %{with python}
%files -n python3-manifold
%defattr(644,root,root,755)
%{py3_sitedir}/manifold3d.cpython-313-i386-linux-gnu.so
%{py3_sitedir}/manifold3d.pyi
%endif
