Name:           perl-Filter
Version:        1.49
Release: 3%{?dist}.0.2
Summary:        Perl source filters
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Filter/
Source0:        http://www.cpan.org/modules/by-module/Filter/Filter-%{version}.tar.gz
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(strict)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Test::More)
# Optional tests
BuildRequires:  perl(POSIX)
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::Pod) >= 1.00
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

Prefix: %{_prefix}

%description
Source filters alter the program text of a module before Perl sees it, much as
a C preprocessor alters the source text of a C program before the compiler
sees it.

%prep
%setup -q -n Filter-%{version}
# Clean examples
find examples -type f -exec chmod -x -- {} +
sed -i -e '1 s|.*|#!%{__perl}|' examples/filtdef

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" \
  PREFIX=%{_prefix} \
  INSTALLVENDORLIB=%{perl_vendorlib} \
  INSTALLVENDORARCH=%{perl_vendorarch}
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%files
%license README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Filter*

%exclude %{_mandir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.49-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.49-2
- Mass rebuild 2013-12-27

* Thu Apr 04 2013 Petr Pisar <ppisar@redhat.com> - 1.49-1
- 1.49 bump

* Wed Apr 03 2013 Petr Pisar <ppisar@redhat.com> - 1.48-1
- 1.48 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.45-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 1.45-2
- Perl 5.16 rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 1.45-1
- 1.45 bump

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.43-3
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 1.43-2
- Skip optional Test::Pod on bootstraping perl

* Mon Feb 27 2012 Petr Pisar <ppisar@redhat.com> - 1.43-1
- 1.43 bump

* Tue Feb 14 2012 Petr Pisar <ppisar@redhat.com> 1.39-1
- Specfile autogenerated by cpanspec 1.78.
