Name:          file
Version:       5.39
Release:       1
Summary:       A tool to identify the type of a particular file type
License:       BSD
URL:           http://www.darwinsys.com/file/
Source0:       ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz

Patch1:	       0001-file-localmagic.patch

Requires: %{name}-libs = %{version}-%{release}
BuildRequires: autoconf automake libtool git zlib-devel

%description
The program checks to see if the file is empty,or if
its some sort of special file. Any known file types
appropriate to the system you are running on (sockets,
symbolic links, or named pipes (FIFOs) on those systems
that implement them) are intuited if they are defined
in the system header file

%package libs
Summary: Libraries for applications that use libmagic
License: BSD

%description libs
This package contains libraries for applications that use libmagic.

%package devel
Summary:   Libraries and header files for file development
Requires:  %{name}-libs%{?_isa} = %{version}-%{release}
Provides:  %{name}-static %{name}-static%{?_isa}
Obsoletes: %{name}-static

%description devel
This package contains files needed to develop applications that use
file header files and libmagic library

%package help
Summary: Including man files for file
Requires: man

%description help
This contains man files for the using of file

%package -n python2-magic
Summary: Python 2 bindings for the libmagic API
Requires: %{name} = %{version}-%{release}
BuildRequires: python2-devel
BuildArch: noarch
%{?python_provide:%python_provide python2-magic}

%description -n python2-magic
This package contains the Python 2 bindings to access the libmagic
API. The libmagic library is also used by the familiar file(1) command.

%package -n python3-magic
Summary: Python 3 bindings for the libmagic API
Requires: %{name} = %{version}-%{release}
BuildRequires: python3-devel
BuildArch: noarch

%description -n python3-magic
This package contains the Python 3 bindings to access to the libmagic
API. The libmagic library is also used by the familiar file(1) command.

%prep
%autosetup -p1 -S git

iconv doc/libmagic.man -f iso-8859-1 -t utf-8 -o doc/libmagic.man_
touch -r doc/libmagic.man doc/libmagic.man_
mv doc/libmagic.man_ doc/libmagic.man

rm -rf %{py3dir}
cp -dR python %{py3dir}

%build
autoreconf -fi

CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE" \
%configure --enable-fsect-man5 --disable-rpath --enable-static
sed -i 's/^hardcode_libdir_flag_spec=.*/hardcode_libdir_flag_spec=""/g' libtool
sed -i 's/^runpath_var=LD_RUN_PATH/runpath_var=DIE_RPATH_DIE/g' libtool
export LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/src/.libs
make %{?_smp_mflags} V=1
cd python
CFLAGS="%{optflags}" %{__python2} setup.py build
cd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build

%install
cd ${RPM_BUILD_ROOT}
mkdir -p .%{_bindir} .%{_sysconfdir} .%{_mandir}/man1 .%{_mandir}/man5 .%{_datadir}/misc .%{_datadir}/file
cd -

%make_install
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cp -dR ./magic/magic.local ${RPM_BUILD_ROOT}%{_sysconfdir}/magic
cat magic/Magdir/* > ${RPM_BUILD_ROOT}%{_datadir}/misc/magic
ln -s misc/magic ${RPM_BUILD_ROOT}%{_datadir}/magic
ln -s ../magic ${RPM_BUILD_ROOT}%{_datadir}/file/magic

cd python
%{__python2} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
cd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
%{__install} -d ${RPM_BUILD_ROOT}%{_datadir}/%{name}

%ldconfig_scriptlets libs

%check
#make check

%files
%doc ChangeLog README
%license COPYING
%config(noreplace) %{_sysconfdir}/magic
%{_bindir}/*

%files libs
%doc ChangeLog README
%license COPYING
%{_libdir}/*so.*
%{_datadir}/magic*
%{_datadir}/file
%{_datadir}/misc/*

%files devel
%{_libdir}/*.so
%{_libdir}/libmagic.a
%{_includedir}/magic.h
%{_libdir}/pkgconfig/libmagic.pc

%files help
%{_mandir}/man*

%files -n python2-magic
%doc python/README.md python/example.py
%{!?_licensedir:%global license %%doc}
%license COPYING
%{python2_sitelib}/magic.py
%{python2_sitelib}/magic.pyc
%{python2_sitelib}/magic.pyo
%{python2_sitelib}/*egg-info

%files -n python3-magic
%doc python/README.md python/example.py
%{!?_licensedir:%global license %%doc}
%license COPYING
%{python3_sitelib}/magic.py
%{python3_sitelib}/*egg-info
%{python3_sitelib}/__pycache__/*

%changelog
* Tue Jul 21 2020 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 5.39-1
- update to 5.39 version and tmp remove 'make check'

* Sat Mar 28 2020 hy <eulerstoragemt@huawei.com> - 5.38-2
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESC:add make check

* Fri Jan 10 2020 Huangzheng <huangzheng22@huawei.com> - 5.38-1
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESC:upgrade package

* Thu Dec 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.34-9
- reupload patches

* Wed Dec 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.34-8
- revert patches

* Tue Dec 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.34-7
- some bugs fix

* Wed Sep 11 2019 huangzheng <huangzheng22@huawei.com> - 5.34-6
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:openEuler Debranding, build libs package again

* Mon Sep 9 2019 huangzheng <huangzheng22@huawei.com> - 5.34-5
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:openEuler Debranding

* Tue Aug 20 2019 zhanghaibo <ted.zhang@huawei.com> - 5.34-4
- correct patch name
