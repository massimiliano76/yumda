%define _trivial .0
%define _buildid .1
%global reldate 20130402

Name:		json-c
Version:	0.11
Release: 4%{?dist}.0.3
Summary:	A JSON implementation in C
Group:		Development/Libraries
License:	MIT
URL:		https://github.com/json-c/json-c/wiki
Source0:	https://github.com/json-c/json-c/archive/json-c-%{version}-%{reldate}.tar.gz

Patch0:		json-c-CVE-2013-6371.patch

#amazon patches
Patch500: json-c-fallthrough.diff

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: libtool

%description
JSON-C implements a reference counting object model that allows you to easily
construct JSON objects in C, output them as JSON formatted strings and parse
JSON formatted strings back into the C representation of JSON objects.

%package devel
Summary:	Development headers and library for json-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the development headers and library for json-c.


%package doc
Summary:	Reference manual for json-c
Group:		Documentation
%if 0%{?fedora} > 10 || 0%{?rhel}>5
BuildArch:	noarch
%endif

%description doc
This package contains the reference manual for json-c.

%prep
%setup -q -n json-c-json-c-%{version}-%{reldate}

%patch0 -p1 -b .cve20136371
%patch500 -p1 -b .fallthrough

for doc in ChangeLog; do
 iconv -f iso-8859-1 -t utf8 $doc > $doc.new &&
 touch -r $doc $doc.new &&
 mv $doc.new $doc
done

# regenerate auto stuff to avoid rpath issue
autoreconf -fi


%build
%configure \
  --enable-shared \
  --disable-static \
  --disable-rpath \
  --enable-rdrand
# parallel build is broken for now, make %{?_smp_mflags}
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Get rid of la files
rm -rf %{buildroot}%{_libdir}/*.la

# yum cannot replace a dir by a link
# so switch the dir names
rm %{buildroot}%{_includedir}/json
mv %{buildroot}%{_includedir}/json-c \
   %{buildroot}%{_includedir}/json
ln -s json \
   %{buildroot}%{_includedir}/json-c


%check
make check


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README README.html
%{_libdir}/libjson.so.*
%{_libdir}/libjson-c.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/json
%{_includedir}/json-c
%{_libdir}/libjson.so
%{_libdir}/libjson-c.so
%{_libdir}/pkgconfig/json.pc
%{_libdir}/pkgconfig/json-c.pc

%files doc
%defattr(-,root,root,-)
%doc doc/html/*


%changelog
* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 0.11-4
- fix has collision CVE-2013-6371
- fix buffer overflow CVE-2013-6370
- enable upstream test suite

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.11-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.11-2
- Mass rebuild 2013-12-27

* Mon Apr 29 2013 Remi Collet <remi@fedoraproject.org> - 0.11-1
- update to 0.11
- fix source0
- enable both json and json-c libraries

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 24 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.10-2
- Compile and install json_object_iterator using Remi Collet's fix (BZ #879771).

* Sat Nov 24 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.10-1
- Update to 0.10 (BZ #879771).

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 23 2012 Jiri Pirko <jpirko@redhat.com> - 0.9-4
- add json_tokener_parse_verbose, and return NULL on parser errors

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Apr 06 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.9-1
- First release.
