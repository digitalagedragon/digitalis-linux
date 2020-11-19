%define system_python 3.9

# If host == target, we aren't building cross tools.
# We should install into /usr and package headers.
%if "%{_host}" == "%{_target}"
%define isnative 1
%else
# Otherwise, we are building a cross tool, to be installed into a sysroot at
# /usr/arch-vendor-os-abi/.
%define isnative 0
%define cross %{_target}-
%define _prefix /usr/%{_target}/usr
%endif

Name:           %{?cross}rpm
Version:        4.16.0
Release:        3%{?dist}
Summary:        The RPM Package Manager (RPM) is a powerful package management system.

License:        GPLv2
URL:            https://rpm.org/
%undefine       _disable_source_fetch
Source0:        http://ftp.rpm.org/releases/rpm-4.16.x/rpm-%{version}.tar.bz2
%define         SHA256SUM0 ca5974e9da2939afb422598818ef187385061889ba766166c4a3829c5ef8d411

# X10-Update-Spec: { "type": "webscrape", "url": "http://rpm.org/timeline", "pattern": "RPM ((?:\\d+\\.?)+) released" }

Patch0:         rpm-0001-use-sqlite.patch
Patch1:         rpm-0002-enable-debugpkgs.patch

%if "%{_build}" != "%{_host}"
%define host_tool_prefix %{_host}-
%endif

%if "%{_host}" != "%{_target}"
%define target_tool_prefix %{_target}-
%else
%define target_tool_prefix %{?host_tool_prefix}
%endif

BuildRequires:  %{?target_tool_prefix}gcc %{?target_tool_prefix}zlib-devel
BuildRequires:  %{?target_tool_prefix}libgcrypt-devel %{?target_tool_prefix}libmagic-devel %{?target_tool_prefix}libpopt-devel
BuildRequires:  %{?target_tool_prefix}libarchive-devel %{?target_tool_prefix}libsqlite-devel %{?target_tool_prefix}pkg-config
BuildRequires:  %{?target_tool_prefix}liblua-devel
BuildRequires:  %{?target_tool_prefix}libpython%{system_python}-devel
BuildRequires:  %{?target_tool_prefix}libzstd-devel
BuildRequires:  %{?target_tool_prefix}libelf-devel

BuildRequires:  make

Requires:       xz
Requires:       tar
Requires:       bzip2
Requires:       elfutils
Requires:       patch
Requires:       curl

Requires:       digitalis-rpm-macros

Requires:       %{?cross}librpm = %{version}-%{release}

%undefine _annotated_build

%description

%package     -n %{?cross}librpm
Summary:        A library for handling RPM packages.
License:        GPLv2
URL:            https://rpm.org/

%description -n %{?cross}librpm

%package     -n %{?cross}librpm-devel
Summary:        Development files for librpm
Requires:       %{?cross}librpm%{?_isa} = %{version}-%{release}
Requires:       %{?cross}libgcrypt-devel %{?cross}zlib-devel %{?cross}libpopt-devel %{?cross}libsqlite-devel
Requires:       %{?cross}libzstd-devel
Requires:       %{?cross}libarchive-devel

%description -n %{?cross}librpm-devel
The librpm-devel package contains libraries and header files for
developing applications that use librpm.


%prep
echo "%SHA256SUM0  %SOURCE0" | sha256sum -c -
%autosetup -p1 -n rpm-%{version}
sed -i '1s/python/python3/' scripts/pythondistdeps.py

%build
export PYTHON=python%{system_python}
%configure --libdir=%{_prefix}/lib --host=%{_target} --enable-bdb=no --enable-sqlite=yes --disable-openmp --enable-python
%make_build

%install
%make_install
%find_lang rpm

find %{buildroot} -name '*.la' -exec rm -f {} ';'

# TODO... just TODO
rm %{buildroot}%{_prefix}/lib/rpm/fileattrs/perl*.attr

%files -f rpm.lang
%license COPYING
# TODO split rpmbuild out
%{_bindir}/*
%doc %{_mandir}/man{1,8}/*
%doc %{_mandir}/*/man{1,8}/*

%files -n %{?cross}librpm
%{_prefix}/lib/*.so.*
%{_prefix}/lib/rpm-plugins
%{_prefix}/lib/rpm
%{_prefix}/lib*/python%{system_python}/site-packages/rpm

%files -n %{?cross}librpm-devel
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*.pc
%{_includedir}/rpm

%changelog

- 2020-11-18 Morgan Thomas <m@m0rg.dev> 4.16.0 release 3
  Updated to Python 3.9

- 2020-11-18 Morgan Thomas <m@m0rg.dev> 4.16.0 release 2
  Split the distro-specific RPM macros out to their own package.

- 2020-11-07 Morgan Thomas <m@m0rg.dev> <no version change>
  Explicitly set PYTHON.
