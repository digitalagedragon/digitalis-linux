Name:           dnf
Version:        4.2.6
Release:        1%{?dist}
Summary:        A powerful RPM-based package manager

License:        GPLv2
URL:            https://github.com/rpm-software-management/dnf
%undefine       _disable_source_fetch
Source0:        https://github.com/rpm-software-management/dnf/archive/%{version}.tar.gz#/dnf-%{version}.tar.gz
%define         SHA256SUM0 7357cddca06cfe6fb79f4e3c758006d0c9071e151289ea91497b5836321400cc

%if "%{_build}" != "%{_host}"
%define host_tool_prefix %{_host}-
BuildRequires: %{?host_tool_prefix}cmake-toolchain
%endif

BuildRequires:  %{?host_tool_prefix}gcc
BuildRequires:  %{?host_tool_prefix}librpm-devel
BuildRequires:  %{?host_tool_prefix}libsolv-devel
BuildRequires:  %{?host_tool_prefix}libdnf-devel
BuildRequires:  %{?host_tool_prefix}libcomps-devel
BuildRequires:  make
BuildRequires:  cmake

Requires:       libdnf
Requires:       libcomps
Requires:       rpm

%undefine _annotated_build
%global debug_package %{nil}

%description

%prep
echo "%SHA256SUM0  %SOURCE0" | sha256sum -c -
%autosetup

%build
mkdir build
cd build
cmake \
%if "%{_build}" != "%{_target}"
    -DCMAKE_TOOLCHAIN_FILE=/usr/%{_target}/cmake_toolchain \
%endif
    -DCMAKE_INSTALL_PREFIX=%{_prefix} -DPYTHON_DESIRED=3 -DWITH_MAN=0 ..
%make_build

%install
cd build
%make_install

ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-3 %{buildroot}%{_bindir}/dnf-automatic
install -dm755 %{buildroot}%{_sysconfdir}/yum.repos.d

%files
%license COPYING
%{_bindir}/*
%{_prefix}/lib/python3.8/site-packages/dnf
%{_prefix}/lib/tmpfiles.d
%exclude %{_prefix}/lib/systemd
%config %{_sysconfdir}/libreport
%config %{_sysconfdir}/dnf
%config %{_sysconfdir}/logrotate.d/dnf
%config %{_sysconfdir}/bash_completion.d/dnf
%dir %{_sysconfdir}/yum.repos.d

%changelog