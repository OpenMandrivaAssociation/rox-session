%define oname ROX-Session
%define name rox-session
%define appdir %_prefix/lib/apps
Name:		%name
Version:	0.30
Release:    7
Summary:	Session manager for the ROX graphical desktop
Group:		Graphical desktop/Other
License:	GPL
URL:		http://rox.sourceforge.net/rox_session.php3
Source:		http://prdownloads.sourceforge.net/rox/%{name}-%{version}.tar.bz2
Source1:	rox-session
Source2:	%name-48.png
Source3:	%name-32.png
Source4:	%name-16.png
Patch1: rox-session-0.26-suppress-error.patch
Requires:	rox-lib
Requires: 	python
Requires:	python-dbus
BuildArch: noarch

%description
ROX-Session is a really simple session manager. It loads, runs any
programs you asked it to, and then quits when you run it a second time
(thus ending your session). It does not display any windows until you
ask it to quit.

The first time you run it it will offer to make itself your session
manager (so that you'll get a ROX desktop when you log in).

%prep
%setup -q
%patch1 -p1
chmod 644 %oname/*.xml

%build
rm -f %oname/Messages/*.p?
rm -f %oname/Messages/update-po
rm -f %oname/Messages/dist

%install
rm -rf $RPM_BUILD_ROOT %name.lang
mkdir -p $RPM_BUILD_ROOT%appdir
cp -a ./%oname $RPM_BUILD_ROOT%appdir
rm -rf %buildroot%appdir/%oname/{src,build}

#rox session entry
mkdir -p %{buildroot}%{_sysconfdir}/X11/wmsession.d
cat << EOF > %{buildroot}%{_sysconfdir}/X11/wmsession.d/17Rox
NAME=ROX
ICON=%name.png
DESC=Session manager for the ROX desktop
EXEC=%{_bindir}/rox-session
SCRIPT:
exec %{_bindir}/rox-session
EOF

#session script
mkdir -p %buildroot%_bindir
cp %SOURCE1 %buildroot%_bindir/%name
#gw path to the ROX-Session directory
perl -pi -e "s^%%s^%appdir/%oname^" %buildroot%_bindir/%name

#session icons
mkdir -p %buildroot{%_iconsdir,%_miconsdir,%_liconsdir}
install -m 644 %SOURCE2 %buildroot%_liconsdir/%name.png
install -m 644 %SOURCE3 %buildroot%_iconsdir/%name.png
install -m 644 %SOURCE4 %buildroot%_miconsdir/%name.png

for gmo in %buildroot%appdir/%oname/Messages/*.gmo;do
echo "%lang($(basename $gmo|sed s/.gmo//)) $(echo $gmo|sed s!%buildroot!!)" >> %name.lang
done


%files -f %name.lang
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/17Rox
%attr(755,root,root) %{_bindir}/rox-session
%doc %appdir/%oname/Help
%dir %appdir/%oname
%appdir/%oname/.DirIcon
%appdir/%oname/browser
%appdir/%oname/AppRun
%appdir/%oname/Login
%appdir/%oname/RunROX
%appdir/%oname/Setup*
%appdir/%oname/Styles
%appdir/%oname/*.*
%appdir/%oname/images
%appdir/%oname/tests
%dir %appdir/%oname/Messages
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png



%changelog
* Thu May 07 2009 Gustavo De Nardin <gustavodn@mandriva.com> 0.30-5mdv2010.0
+ Revision: 372808
- fixed oroborox WM name
- use bunzipped file
- bunzip2 plain text file

* Sat Aug 02 2008 Thierry Vignaud <tvignaud@mandriva.com> 0.30-4mdv2009.0
+ Revision: 260303
- rebuild

* Mon Jul 28 2008 Thierry Vignaud <tvignaud@mandriva.com> 0.30-3mdv2009.0
+ Revision: 251444
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0.30-1mdv2008.1
+ Revision: 140747
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Apr 17 2007 GÃ¶tz Waschk <waschk@mandriva.org> 0.30-1mdv2007.1
+ Revision: 13565
- new version


* Mon Sep 11 2006 Götz Waschk <waschk@mandriva.org> 0.29-1mdv2007.0
- New version 0.29

* Mon Jul 31 2006 GÃ¶tz Waschk <waschk@mandriva.org> 0.28-1mdv2007.0
- Rebuild

* Sat Mar 11 2006 Götz Waschk <waschk@mandriva.org> 0.28-1mdk
- update file list
- New release 0.28

* Mon Feb 13 2006 Götz Waschk <waschk@mandriva.org> 0.27-1mdk
- it is noarch now
- drop patch 0
- new source URL
- new version

* Wed Jan 25 2006 GÃ¶tz Waschk <waschk@mandriva.org> 0.26-5mdk
- rebuild for new dbus
- use mkrel

* Wed Oct 26 2005 GÃ¶tz Waschk <waschk@mandriva.org> 0.26-4mdk
- rebuild for new dbus

* Thu Oct 13 2005 Götz Waschk <waschk@mandriva.org> 0.26-3mdk
- update session script (source 1)
- patch1 to suppress error about 0which

* Sun Aug 28 2005 Götz Waschk <waschk@mandriva.org> 0.26-2mdk
- reebable fortify

* Sun Aug 28 2005 Götz Waschk <waschk@mandriva.org> 0.26-1mdk
- update paths
- disable fortify
- New release 0.26

* Thu Aug 11 2005 GÃ¶tz Waschk <waschk@mandriva.org> 0.1.25-2mdk
- Rebuild

* Thu Oct 14 2004 Goetz Waschk <waschk@linux-mandrake.com> 0.1.25-1mdk
- New release 0.1.25

* Fri Aug 20 2004 Götz Waschk <waschk@linux-mandrake.com> 0.1.24-1mdk
- fix source URL
- New release 0.1.24

* Fri Jun 11 2004 Götz Waschk <waschk@linux-mandrake.com> 0.1.23-1mdk
- patch to prefer oroborox if installed
- New release 0.1.23

* Tue Apr 27 2004 Götz Waschk <waschk@linux-mandrake.com> 0.1.22-2mdk
- update source1

* Mon Apr 26 2004 Götz Waschk <waschk@linux-mandrake.com> 0.1.22-1mdk
- fix file listing
- requires dbus
- cvs snapshot

* Sun Oct 26 2003 Götz Waschk <waschk@linux-mandrake.com> 0.1.21-1mdk
- new version

