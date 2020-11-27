Name:           bc
Version:        3.2.1
Release:        1%{?dist}
Summary:        bc is an arbitrary precision numeric processing language.

License:        BSD-2-Clause
URL:            https://git.yzena.com/gavin/bc
%undefine       _disable_source_fetch
Source0:        https://git.yzena.com/gavin/bc/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%define         SHA256SUM0 47ee81c65a329c01674a8b11b41694844f7ee476404cde8e8b1ae4b1b7b21543

# X10-Update-Spec: { "type": "git-tags", 
# X10-Update-Spec:   "repo": "https://git.yzena.com/gavin/bc.git", 
# X10-Update-Spec:   "pattern": "^(\\d+\\.\\d+\\.\\d+)$" }

%if "%{_build}" != "%{_host}"
%define host_tool_prefix %{_host}-
%endif

BuildRequires:  %{?host_tool_prefix}gcc
BuildRequires:  gcc
BuildRequires:  make

%undefine _annotated_build
%global debug_package %{nil}

%description

%prep
echo "%SHA256SUM0  %SOURCE0" | sha256sum -c -
%autosetup -n %{name}

%build
PREFIX=%{_prefix} HOSTCC=gcc CC=%{?host_tool_prefix}gcc CFLAGS="-std=c99" ./configure.sh -g -O3
%make_build

%install
DESTDIR=%{buildroot} make install

%files
%license LICENSE.md
%{_bindir}/bc
%{_bindir}/dc
%{_datadir}/locale/*/bc
%doc %{_mandir}/man1/*

%changelog

* Fri Nov 27 2020 Morgan Thomas <m@m0rg.dev> 3.2.1-1
  Updated to version 3.2.1.

* Wed Nov 18 2020 Morgan Thomas <m@m0rg.dev> 3.1.6-1
  Updated to version 3.1.6.
