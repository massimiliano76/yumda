Name:           perl-Text-ParseWords
Version:        3.29
Release:        4%{?dist}
Summary:        Parse text into an array of tokens or array of arrays
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Text-ParseWords/
Source0:        http://www.cpan.org/authors/id/C/CH/CHORNY/Text-ParseWords-%{version}.tar.gz
Source1:        license.email
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
# Tests:
# Config not used
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)

%description
The nested_quotewords() and quotewords() functions accept a delimiter (which
can be a regular expression) and a list of lines and then breaks those lines
up into a list of words ignoring delimiters that appear inside quotes.
quotewords() returns all of the tokens in a single long list, while
nested_quotewords() returns a list of token lists corresponding to the
elements of @lines. parse_line() does tokenizing on a single string. The
quotewords() functions simply call &parse_line(), so if you're only splitting
one line you can call parse_line() directly and save a function call.

%prep
%setup -q -n Text-ParseWords-%{version}
for F in CHANGES README; do
    tr -d "\r" < "$F" > "${F}.unix"
    touch -r "$F" "${F}.unix"
    mv "${F}.unix" "$F"
done
cp %{SOURCE1} ./

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc CHANGES README license.email
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.29-4
- Mass rebuild 2013-12-27

* Tue Nov 19 2013 Marcela Mašláňová <mmaslano@redhat.com> 3.29-3
- According to guidelines must be email statement added as new source.
- Related: rhbz#1030808

* Tue Nov 19 2013 Marcela Mašláňová <mmaslano@redhat.com> 3.29-2
- Add licence statement from the upstream ticket
- Resolves: rhbz#1030808

* Mon Mar 18 2013 Petr Pisar <ppisar@redhat.com> 3.29-1
- Specfile autogenerated by cpanspec 1.78.
