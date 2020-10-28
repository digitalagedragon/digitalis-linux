Name:           patch
Version:        2.7.6
Release:        1%{?dist}
Summary:        GNU Diffutils is a package of several programs related to finding differences between files.

License:        GPLv3+
URL:            https://www.gnu.org/software/patch
%undefine       _disable_source_fetch
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
%define         SHA256SUM0 ac610bda97abe0d9f6b7c963255a11dcb196c25e337c61f94e4778d632f1d8fd

%if "%{_build}" != "%{_host}"
%define host_tool_prefix %{_host}-
%endif

BuildRequires:  %{?host_tool_prefix}gcc %{?host_tool_prefix}glibc-devel
BuildRequires:  make

%undefine _annotated_build

%description

%prep
echo "%SHA256SUM0  %SOURCE0" | sha256sum -c -
%autosetup

%build
%configure
%make_build

%install
%make_install

%files
%license COPYING
%{_bindir}/*
%doc %{_mandir}/man1/*.gz

%changelog