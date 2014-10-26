Summary:	Library to access weather information from online services for numerous locations
Name:		libmateweather
Version:	1.8.0
Release:	2
License:	GPL v2+
Group:		X11/Libraries
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	f11f7f3c6ae72e58b54931cb09bb76a7
Patch0:		%{name}-Landshut.patch
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libmateweather is a library to access weather information from online
services for numerous locations.

%package devel
Summary:	Header files for libmateweather
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libmateweather.

%package data
Summary:	libmateweather data
Group:		X11/Development/Libraries
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name} = %{version}-%{release}

%description data
libmateweather data.

%package apidocs
Summary:	libmateweather API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libmateweather API documentation.

%prep
%setup -q
%patch0 -p1

# https://bugzilla.gnome.org/show_bug.cgi?id=614645
%{__sed} -i -e 's|mate|hicolor|g' icons/Makefile.am

# kill mate-common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'		\
    -i -e '/MATE_CXX_WARNINGS.*/d'		\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--disable-static		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang libmateweather

find $RPM_BUILD_ROOT -name "Locations.*.xml" | sed 's:'"$RPM_BUILD_ROOT"'::
s:\(.*\)/Locations\.\([^.]*\)\.xml:%lang(\2) \1/Locations.\2.xml:' | sort | uniq >> libmategweather.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%post data
%update_icon_cache hicolor
%update_gsettings_cache

%preun data
%update_icon_cache hicolor
%update_gsettings_cache

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %ghost %{_libdir}/libmateweather.so.?
%attr(755,root,root) %{_libdir}/libmateweather.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmateweather.so
%{_datadir}/libmateweather
%{_includedir}/libmateweather
%{_pkgconfigdir}/mateweather.pc

%files data -f libmateweather.lang
%defattr(644,root,root,755)
%{_datadir}/glib-2.0/schemas/org.mate.weather.gschema.xml
%dir %{_datadir}/libmateweather
%{_datadir}/libmateweather/Locations.xml
%{_iconsdir}/hicolor/*/status/*.png
%{_iconsdir}/hicolor/*/status/*.svg

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}

