%define oname ROX-Session
%define version 0.30
%define name rox-session
%define appdir %_prefix/lib/apps
Name:		%name
Version:	%version
Release: %mkrel 1
Summary:	Session manager for the ROX graphical desktop
Group:		Graphical desktop/Other
License:	GPL
URL:		http://rox.sourceforge.net/rox_session.php3
Source:		http://prdownloads.sourceforge.net/rox/%{name}-%{version}.tar.bz2
Source1:	rox-session.bz2
Source2:	%name-48.png
Source3:	%name-32.png
Source4:	%name-16.png
Patch1: rox-session-0.26-suppress-error.patch
Requires:	rox-lib
Requires: 	python
Requires:	dbus-python
BuildRoot:	%{_tmppath}/%{name}-buildroot
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
bzcat %SOURCE1 > %buildroot%_bindir/%name
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

%clean
rm -rf $RPM_BUILD_ROOT

%post
%make_session

%postun
%make_session

%files -f %name.lang
%defattr (-,root,root)
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

