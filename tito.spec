#
# Conditional build:
%bcond_with	tests	# unit tests

Summary:	A tool for managing rpm based git projects
Name:		tito
Version:	0.6.12
Release:	0.1
License:	GPL v2
Source0:	https://github.com/dgoodwin/tito/archive/%{name}-%{version}-1.tar.gz
# Source0-md5:	03a9f989abe96719befd31c1b4c01db3
Group:		Development/Tools
URL:		https://github.com/dgoodwin/tito
BuildRequires:	asciidoc
BuildRequires:	docbook-style-xsl
BuildRequires:	libxslt
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
BuildRequires:	rpm-build
#BuildRequires:	rpmdevtools
BuildRequires:	which
#Requires:	python3-blessings
#Requires:	python3-bugzilla
Requires:	python3-setuptools
#Requires:	rpm-python3
%if %{with tests}
# todo: add %%check to spec file in accordance with
# https://fedoraproject.org/wiki/QA/Testing_in_check
BuildRequires:	git
BuildRequires:	python-bugzilla
BuildRequires:	python3-bugzilla
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	rpm-python3
%endif
#Requires:	fedora-packager
#Requires:	fedpkg
Requires:	rpm-build
#Requires:	rpmdevtools
Requires:	rpmlint
# Cheetah used not to exist for Python 3, but it's what Mead uses.  We
# install it and call via the command line instead of importing the
# previously potentially incompatible code, as we have not yet got
# around to changing this
Requires:	/usr/bin/cheetah
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tito is a tool for managing tarballs, rpms, and builds for projects
using Git.

%prep
%setup -q -n %{name}-%{name}-%{version}-1
sed -i 1"s|#!.*|#!%{__python3}|" bin/tito

%build
%py3_build
# convert manages
a2x -d manpage -f manpage titorc.5.asciidoc
a2x -d manpage -f manpage tito.8.asciidoc
a2x -d manpage -f manpage tito.props.5.asciidoc
a2x -d manpage -f manpage releasers.conf.5.asciidoc

%install
rm -rf $RPM_BUILD_ROOT
%py3_install
rm -v $RPM_BUILD_ROOT%{py3_sitescriptdir}/*egg-info/requires.txt
# manpages
%{__mkdir_p} $RPM_BUILD_ROOT%{_mandir}/man5
%{__mkdir_p} $RPM_BUILD_ROOT%{_mandir}/man8
cp -a titorc.5 tito.props.5 releasers.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5
cp -a tito.8 $RPM_BUILD_ROOT%{_mandir}/man8
# bash completion facilities
install -Dp share/tito_completion.sh $RPM_BUILD_ROOT%{bash_compdir}/tito

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS doc/*
%attr(755,root,root) %{_bindir}/tito
%attr(755,root,root) %{_bindir}/generate-patches.pl
%{_mandir}/man5/titorc.5*
%{_mandir}/man5/tito.props.5*
%{_mandir}/man5/releasers.conf.5*
%{_mandir}/man8/tito.8*
%{py3_sitescriptdir}/tito
%{py3_sitescriptdir}/tito-*.egg-info
%{bash_compdir}/tito
