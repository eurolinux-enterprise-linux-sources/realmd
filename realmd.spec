Name:		realmd
Version:	0.14.6
Release:	6%{?dist}
Summary:	Kerberos realm enrollment service
License:	LGPLv2+
URL:		http://cgit.freedesktop.org/realmd/realmd/
Source0:	http://www.freedesktop.org/software/realmd/releases/realmd-%{version}.tar.gz
Patch0:		ipa-packages.patch
Patch1:		oddjob-start.patch
Patch2:		safe-printf.patch
Patch3:		missing-fqname.patch

BuildRequires:	intltool pkgconfig
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 2.32.0
BuildRequires:	openldap-devel
BuildRequires:	PackageKit-glib-devel
BuildRequires:	polkit-devel
BuildRequires:	krb5-devel
BuildRequires:	systemd-devel
BuildRequires:	libxslt
BuildRequires:	xmlto
BuildRequires:	automake

Requires:	authconfig
Requires:	oddjob-mkhomedir

%description
realmd is a DBus system service which manages discovery and enrollment in realms
and domains like Active Directory or IPA. The control center uses realmd as the
back end to 'join' a domain simply and automatically configure things correctly.

%package devel-docs
Summary:	Developer documentation files for %{name}

%description devel-docs
The %{name}-devel package contains developer documentation for developing
applications that use %{name}.

%define _hardened_build 1

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=%{buildroot}

%find_lang realmd

%clean

%files -f realmd.lang
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.realmd.conf
%{_sbindir}/realm
%dir %{_libdir}/realmd
%{_libdir}/realmd/realmd
%{_libdir}/realmd/realmd-defaults.conf
%{_libdir}/realmd/realmd-distro.conf
%{_unitdir}/realmd.service
%{_datadir}/dbus-1/system-services/org.freedesktop.realmd.service
%{_datadir}/polkit-1/actions/org.freedesktop.realmd.policy
%doc AUTHORS COPYING ChangeLog NEWS README
%{_mandir}/man8/realm.8.gz
%{_mandir}/man5/realmd.conf.5.gz
%{_localstatedir}/cache/realmd/

%files devel-docs
%doc %{_datadir}/doc/realmd/

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.14.6-6
- Mass rebuild 2014-01-24

* Fri Jan 10 2014 Stef Walter <stefw@redhat.com> - 0.14.6-5
- Don't crash when full_name_format is not in sssd.conf [#1051033]
  This is a regression from a prior update.

* Tue Jan 07 2014 Stef Walter <stefw@redhat.com> - 0.14.6-4
- Fix full_name_format printf(3) related failure [#1048087]

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.14.6-3
- Mass rebuild 2013-12-27

* Fri Sep 20 2013 Stef Walter <stefw@redhat.com> - 0.14.6-2
- Start oddjob after joining a domain [#967023]

* Mon Sep 09 2013 Stef Walter <stefw@redhat.com> - 0.14.6-1
- Update to upstream 0.14.6 point release
- Set 'kerberos method = system keytab' in smb.conf properly [#997580]
- Limit Netbios name to 15 chars when joining AD domain [#1001667]

* Thu Aug 15 2013 Stef Walter <stefw@redhat.com> - 0.14.5-1
- Update to upstream 0.14.5 point release
- Fix regression conflicting --unattended and -U as in --user args [#996223]
- Pass discovered server address to adcli tool [#996995]

* Wed Aug 07 2013 Stef Walter <stefw@redhot.com> - 0.14.4-1
- Update to upstream 0.14.4 point release
- Fix up the [sssd] section in sssd.conf if it's screwed up [#987491]
- Add an --unattended argument to realm command line client [#976593]
- Clearer 'realm permit' manual page example [#985800]

* Mon Jul 22 2013 Stef Walter <stefw@redhat.com> - 0.14.3-1
- Update to upstream 0.14.3 point release
- Populate LoginFormats correctly [#967011]
- Documentation clarifications [#985773] [#967565]
- Set sssd.conf default_shell per domain [#967569]
- Notify in terminal output when installing packages [#984960]
- If joined via adcli, delete computer with adcli too [#967008]
- If input is not a tty, then read from stdin without getpass()
- Configure pam_winbind.conf appropriately [#985819]
- Refer to FreeIPA as IPA [#967019]
- Support use of kerberos ccache to join when winbind [#985817]

* Tue Jun 11 2013 Stef Walter <stefw@redhat.com> - 0.14.2-3
- Run test suite when building the package
- Fix rpmlint errors

* Thu Jun 06 2013 Stef Walter <stefw@redhat.com> - 0.14.2-2
- Install oddjobd and oddjob-mkhomedir when joining domains [#969441]

* Mon May 27 2013 Stef Walter <stefw@redhat.com> - 0.14.2-1
- Update to upstream 0.14.2 version
- Discover FreeIPA 3.0 with AD trust correctly [#966148]
- Only allow joining one realm by default [#966650]
- Enable the oddjobd service after joining a domain [#964971]
- Remove sssd.conf allow lists when permitting all [#965760]
- Add dependency on authconfig [#964675]
- Remove glib-networking dependency now that we no longer use SSL.

* Mon May 13 2013 Stef Walter <stefw@redhat.com> - 0.14.1-1
- Update to upstream 0.14.1 version
- Fix crasher/regression using passwords with joins [#961435]
- Make second Ctrl-C just quit realm tool [#961325]
- Fix critical warning when leaving IPA realm [#961320]
- Don't print out journalctl command in obvious situations [#961230]
- Document the --all option to 'realm discover' [#961279]
- No need to require sssd-tools package [#961254]
- Enable services even in install mode [#960887]
- Use the AD domain name in sssd.conf directly [#960270]
- Fix critical warning when service Release() method [#961385]

* Mon May 06 2013 Stef Walter <stefw@redhat.com> - 0.14.0-1
- Work around broken krb5 with empty passwords [#960001]
- Add manual page for realmd.conf [#959357]
- Update to upstream 0.14.0 version

* Thu May 02 2013 Stef Walter <stefw@redhat.com> - 0.13.91-1
- Fix regression when using one time password [#958667]
- Support for permitting logins by group [#887675]

* Mon Apr 29 2013 Stef Walter <stefw@redhat.com> - 0.13.90-1
- Add option to disable package-kit installs [#953852]
- Add option to use unqualified names [#953825]
- Better discovery of domains [#953153]
- Concept of managing parts of the system [#914892]
- Fix problems with cache directory [#913457]
- Clearly explain when realm cannot be joined [#878018]
- Many other upstream enhancements and fixes

* Wed Apr 17 2013 Stef Walter <stefw@redhat.com> - 0.13.3-2
- Add missing glib-networking dependency, currently used
  for FreeIPA discovery [#953151]

* Wed Apr 17 2013 Stef Walter <stefw@redhat.com> - 0.13.3-1
- Update for upstream 0.13.3 version
- Add dependency on systemd for installing service file

* Tue Apr 16 2013 Stef Walter <stefw@redhat.com> - 0.13.2-2
- Fix problem with sssd not starting after joining

* Mon Feb 18 2013 Stef Walter <stefw@redhat.com> - 0.13.2-1
- Update to upstream 0.13.2 version

* Mon Feb 18 2013 Stef Walter <stefw@redhat.com> - 0.13.1-1
- Update to upstream 0.13.1 version for bug fixes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Stef Walter <stefw@redhat.com> - 0.12-1
- Update to upstream 0.12 version for bug fixes

* Tue Oct 30 2012 Stef Walter <stefw@redhat.com> - 0.11-1
- Update to upstream 0.11 version

* Sat Oct 20 2012 Stef Walter <stefw@redhat.com> - 0.10-1
- Update to upstream 0.10 version

* Wed Oct 17 2012 Stef Walter <stefw@redhat.com> - 0.9-1
- Update to upstream 0.9 version

* Wed Sep 19 2012 Stef Walter <stefw@redhat.com> - 0.8-2
- Add openldap-devel build requirement

* Wed Sep 19 2012 Stef Walter <stefw@redhat.com> - 0.8-1
- Update to upstream 0.8 version
- Add support for translations

* Mon Aug 20 2012 Stef Walter <stefw@redhat.com> - 0.7-2
- Build requires gtk-doc

* Mon Aug 20 2012 Stef Walter <stefw@redhat.com> - 0.7-1
- Update to upstream 0.7 version
- Remove files no longer present in upstream version
- Put documentation in its own realmd-devel-docs subpackage
- Update upstream URLs

* Mon Aug 6 2012 Stef Walter <stefw@redhat.com> - 0.6-1
- Update to upstream 0.6 version

* Tue Jul 17 2012 Stef Walter <stefw@redhat.com> - 0.5-2
- Remove missing SssdIpa.service file from the files list.
  This file will return upstream in 0.6

* Tue Jul 17 2012 Stef Walter <stefw@redhat.com> - 0.5-1
- Update to upstream 0.5 version

* Tue Jun 19 2012 Stef Walter <stefw@redhat.com> - 0.4-1
- Update to upstream 0.4 version
- Cleanup various rpmlint warnings

* Tue Jun 19 2012 Stef Walter <stefw@redhat.com> - 0.3-2
- Add doc files
- Own directories
- Remove obsolete parts of spec file
- Remove explicit dependencies
- Updated License line to LGPLv2+

* Tue Jun 19 2012 Stef Walter <stefw@redhat.com> - 0.3
- Build fixes

* Mon Jun 18 2012 Stef Walter <stefw@redhat.com> - 0.2
- Initial RPM
