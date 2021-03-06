%define _buildid .3

Summary: C library for multiple precision complex arithmetic
Name: libmpc
Version: 1.0.1
Release: 3%{?_buildid}%{?dist}
License: LGPLv3+ and GFDL
Group: Development/Tools
URL: http://www.multiprecision.org/
Source0: http://www.multiprecision.org/mpc/download/mpc-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gmp-devel >= 6.0.0
BuildRequires: mpfr-devel >= 3.1.1
BuildRequires: texinfo

%description
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as Mpfr.

%package devel
Summary: Header and shared development libraries for MPC
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: mpfr-devel gmp-devel

%description devel
Header files and shared object symlinks for MPC is a C library.

%prep
%setup -q -n mpc-%{version}

%build
export CPPFLAGS="%{optflags} -std=gnu99"
export CFLAGS="%{optflags} -std=gnu99"
export EGREP=egrep

%configure --disable-static
make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/libmpc.la
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
if [ -f %{_infodir}/mpc.info.gz ]; then # for --excludedocs
   /sbin/install-info %{_infodir}/mpc.info.gz %{_infodir}/dir || :
fi

%preun devel
if [ $1 = 0 ]; then
   if [ -f %{_infodir}/mpc.info.gz ]; then # for --excludedocs
      /sbin/install-info --delete %{_infodir}/mpc.info.gz %{_infodir}/dir || :
   fi
fi

%files
%defattr(-,root,root,-)
%doc README NEWS COPYING.LESSER
%{_libdir}/libmpc.so.3*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libmpc.so
%{_includedir}/mpc.h
%{_infodir}/*.info*

%changelog
* Wed May 7 2014 Cristian Gafton <gafton@amazon.com>
- import source package RHEL7/libmpc-1.0.1-3.el7

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.0.1-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.1-2
- Mass rebuild 2013-12-27

* Fri Dec 13 2013 Cristian Gafton <gafton@amazon.com>
- import source package RHEL7/libmpc-1.0.1-1.el7

* Thu Dec 12 2013 Cristian Gafton <gafton@amazon.com>
- setup complete for package libmpc

* Tue Feb 19 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.0.1-1
- compat-libmpc (for bootsrapping purposes)
- mpc-1.0.1
- update Source URLs
- fix License: tag

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.0-2
- %%files: track lib soname (so bumps aren't a surprise)
- tighten subpkg deps (%%_isa)
- %%build: --disable-static

* Thu Aug  2 2012 Petr Machata <pmachata@redhat.com> - 1.0-1
- Upstream 1.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Feb 4 2012 Cristian Gafton <gafton@amazon.com>
- update to version 0.8.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.9-1.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 0.9-1.1
- rebuild with new gmp

* Wed Jul 20 2011 Cristian Gafton <gafton@amazon.com>
- import source package EPEL6/libmpc-0.8-3.el6

* Tue Jul 19 2011 Cristian Gafton <gafton@amazon.com>
- setup complete for package libmpc

* Wed Jun 22 2011 <pmachata@redhat.com> - 0.9-1
- Upstream 0.9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-0.3.svn855
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 30 2010 Petr Machata <pmachata@redhat.com> - 0.8.3-0.2.svn855
- Bump for rebuild against the new mpfr

* Fri Nov 19 2010 Petr Machata <pmachata@redhat.com> - 0.8.3-0.1.svn855
- Devel updates (to-be-0.8.3, SVN release 855)
  - New functions mpc_set_dc, mpc_set_ldc, mpc_get_dc, mpc_get_ldc
  - Speed-up mpc_pow_si and mpc_pow_z
  - Bug fixes in trigonometric functions, exp, sqrt
- Upstream 0.8.2
  - Speed-up mpc_pow_ui
- Adjust BuildRequires
- Resolves: #653931

* Wed Jan 20 2010 Petr Machata <pmachata@redhat.com> - 0.8.1-1
- Upstream 0.8.1
  - acosh, asinh, atanh: swap of precisions between real and imaginary parts
  - atan: memory leak
  - log: wrong ternary value in data file; masked by bug in Mpfr 2.4.1
- Resolves: #555471 FTBFS libmpc-0.8-3.fc13

* Fri Nov 13 2009 Petr Machata <pmachata@redhat.com> - 0.8-3
- Require mpfr-devel, gmp-devel in -devel subpackage
- Don't pass --entry to install-info

* Thu Nov 12 2009 Petr Machata <pmachata@redhat.com> - 0.8-2
- Rename the package to libmpc, it's a better choice of name
- %%preun should uninstall mpc's info page, not make's
- Move info page to -devel
- BR on -devel packages
- Drop postscript documentation

* Thu Nov 12 2009 Petr Machata <pmachata@redhat.com> - 0.8-1
- Initial package.
