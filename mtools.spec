Summary: Programs for accessing MS-DOS disks without mounting the disks
Name: mtools
Version: 4.0.12
Release: 1%{?dist}
License: GPLv2+
Group: Applications/System
Source0: ftp://ftp.gnu.org/gnu/mtools/mtools-%{version}.tar.bz2
Url: http://mtools.linux.lu/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0: mtools-3.9.6-config.patch
Requires: info

BuildRequires: texinfo, autoconf

%description
Mtools is a collection of utilities for accessing MS-DOS files.
Mtools allow you to read, write and move around MS-DOS filesystem
files (normally on MS-DOS floppy disks).  Mtools supports Windows95
style long file names, OS/2 XDF disks, and 2m disks

Mtools should be installed if you need to use MS-DOS disks

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .conf

# Correct system paths
for all in mtools.5 mtools.texi; do
	sed -i.orig 's/\/usr\/local//' $all
done

%build
autoreconf -fiv
%configure --disable-floppyd
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc $RPM_BUILD_ROOT/%{_infodir}
%makeinstall
install -m644 mtools.conf $RPM_BUILD_ROOT/etc
gzip -9f $RPM_BUILD_ROOT/%{_infodir}/*

# We aren't shipping this.
find $RPM_BUILD_ROOT -name "floppyd*" -exec rm {} \;

# dir.gz is handled in %%post and %%preun sections
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_infodir}/mtools.info ]; then
    /sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :;
fi

%preun
if [ "$1" -eq 0 ]; then
    if [ -f %{_infodir}/mtools.info ]; then
        /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :;
    fi
fi

%files
%defattr(-,root,root)
%config(noreplace) /etc/mtools.conf
%doc COPYING README Release.notes
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/mtools.info*

%changelog
* Tue Nov 10 2009 Adam Tkac <atkac redhat com> 4.0.12-1
- update to 4.0.12

* Tue Sep 01 2009 Adam Tkac <atkac redhat com> 4.0.11-1
- update to 4.0.11

* Tue Aug 11 2009 Adam Tkac <atkac redhat com> 4.0.10-4
- fix installation with --excludedocs (#515932)

* Tue Aug 11 2009 Adam Tkac <atkac redhat com> 4.0.10-3
- correct source URL

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 04 2009 Adam Tkac <atkac redhat com> 4.0.10-1
- update to 4.0.10

* Mon Mar 09 2009 Adam Tkac <atkac redhat com> 4.0.9-1
- updated to 4.0.9
- merged mtools-3.9.7-bigdisk.patch to config patch
- mtools400-rh480112.patch merged to upstream

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Adam Tkac <atkac redhat com> 4.0.0-3
- fixed off-by-two error in unix_name function (#480112)

* Mon Jan 12 2009 Adam Tkac <atkac redhat com> 4.0.0-2
- don't ship infodir/dir.gz (#478322)

* Mon Dec 01 2008 Adam Tkac <atkac redhat com> 4.0.0-1
- updated to 4.0.0

* Wed Nov 19 2008 Adam Tkac <atkac redhat com> 4.0.0-0.1.pre2
- updated to 4.0.0_pre2

* Tue Nov 11 2008 Adam Tkac <atkac redhat com> 4.0.0-0.1.pre1
- updated to 4.0.0_pre1

* Fri Oct 03 2008 Adam Tkac <atkac redhat com> 3.9.11-5
- mtools-3.9.9-noargs.patch and mtools-3.9.6-paths.patch are not needed
- rebuild (#465040)

* Tue Feb 19 2008 Adam Tkac <atkac redhat com> 3.9.11-4
- fixed building on x86_64 (build with --disable-floppyd)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.9.11-3.1
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Adam Tkac <atkac redhat com> 3.9.11-2.1
- corrected post and preun sections (#428478)
- fix rpmlint errors
- start use autoreconf

* Wed Aug 22 2007 Adam Tkac <atkac redhat com> 3.9.11-2
- rebuild (BuildID feature)
- change license to GPLv2+

* Wed May 31 2007 Adam Tkac <atkac redhat com> 3.9.11-1
- updated to latest upstream (3.9.11)

* Fri May 11 2007 Adam Tkac <atkac redhat com> 3.9.10-7
- in the end script has been completely rewriten by <skasal@redhat.com>

* Fri May 11 2007 Adam Tkac <atkac redhat com> 3.9.10-6
- some minor changes in sh patch (changed sh to bash)

* Fri May 11 2007 Adam Tkac <atkac redhat com> 3.9.10-5
- patch to #239741 by Matej Cepl <mcepl@redhat.com>
  (rewrites /usr/bin/amuFormat.sh to /bin/sh)

* Tue Feb 05 2007 Adam Tkac <atkac redhat com> 3.9.10-4
- fixed some unstandard statements in spec file (#226162)

* Mon Jan 22 2007 Adam Tkac <atkac redhat com> 3.9.10-3
- Resolves: #223712
- applied Ville Skytta's (ville.skytta "antispam" iki.fi) patch
  (install-info scriptlet failures)

* Wed Aug 09 2006 Jitka Kudrnacova <jkudrnac@redhat.com> - 3.9.10-2
- rebuilt to prevent corruption on the 13th character (#195528)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.9.10-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.9.10-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.9.10-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Oct 19 2005 Tim Waugh <twaugh@redhat.com> 3.9.10-1
- 3.9.10.

* Mon Mar 21 2005 Tim Waugh <twaugh@redhat.com> 3.9.9-13
- Fixed memset() usage bug.

* Tue Mar 15 2005 Tim Waugh <twaugh@redhat.com> 3.9.9-12
- Fix build (bug #151135).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 3.9.9-11
- Rebuild for new GCC.

* Fri Dec 10 2004 Tim Waugh <twaugh@redhat.com> 3.9.9-10
- Fixed mpartition --help output (bug #65293).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan  8 2004 Tim Waugh <twaugh@redhat.com> 3.9.9-7
- Fix mistaken use of '&' instead of '&&'.

* Tue Dec  9 2003 Tim Waugh <twaugh@redhat.com> 3.9.9-6
- Remove last (incorrect) change.

* Tue Dec  9 2003 Tim Waugh <twaugh@redhat.com> 3.9.9-5
- Fix mistaken variable assignment in comparison (bug #110823).

* Thu Nov 27 2003 Tim Waugh <twaugh@redhat.com>
- Build requires texinfo (bug #111000).

* Sat Oct 25 2003 Tim Waugh <twaugh@redhat.com> 3.9.9-4
- Rebuilt.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 22 2003 Tim Waugh <twaugh@redhat.com> 3.9.9-2
- Fix mcomp with no arguments (bug #91372).

* Tue Mar 18 2003 Tim Waugh <twaugh@redhat.com> 3.9.9-1
- 3.9.9.
- Add config lines for hpoj photo-card access on drive P:.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebuilt in current collinst

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.9.8-2
- Add patch from maintainer

* Mon May 28 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.9.8-1
- 3.9.8 final

* Mon May 21 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.9.8-0.pre1.0
- 3.9.8pre1

* Wed May 16 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.9.7-6
- Fix support for disks > 1.44 MB (#40857)

* Tue May  8 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.9.7-5
- Update to 20010507

* Wed Jan 10 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Apply the author's current patches, fixes among other things
  ZIP drive support and doesn't crash when trying to access a BSD disk

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Trond Eivind Glomsrod <teg@redhat.com>
- specify ownership

* Wed Jun 07 2000 Trond Eivind Glomsrod <teg@redhat.com>
- Version 3.9.7
- use %%{_mandir}, %%{_makeinstall}, %%configure, %%makeinstall
  and %%{_tmppath}

* Wed Feb 09 2000 Cristian Gafton <gafton@redhat.com>
- get rid of mtools.texi as a doc file (we have the info file)
- fix config file so mtools work (#9264)
- fix references to the config file to be /etc/mtools.conf

* Fri Feb  4 2000 Bill Nottingham <notting@redhat.com>
- expunge floppyd

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description
- version 3.9.6

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- patch to make the texi sources compile
- fix the spec file group and description
- fixed floppy drive sizes

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0
- fixed invalid SAMPLE_FILE configuration file

* Wed Sep 02 1998 Michael Maher <mike@redhat.com>
- Built package for 5.2.
- Updated Source to 3.9.1.
- Cleaned up spec file.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- updated to 3.8

* Tue Oct 21 1997 Otto Hammersmith
- changed buildroot to /var/tmp, rather than /tmp
- use install-info

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Apr 17 1997 Erik Troan <ewt@redhat.com>
- Changed sysconfdir to be /etc

* Mon Apr 14 1997 Michael Fulbright <msf@redhat.com>
- Updated to 3.6
