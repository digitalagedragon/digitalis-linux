Name:           gzip
Version:        1.10
Release:        1%{?dist}
Summary:        GNU Gzip is a popular data compression program.

License:        GPLv3+
URL:            https://www.gnu.org/software/gzip
%undefine       _disable_source_fetch
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
%define         SHA256SUM0 8425ccac99872d544d4310305f915f5ea81e04d0f437ef1a230dc9d1c819d7c0

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
install -dm755 %{buildroot}/%{_bindir}/../../bin
mv -v %{buildroot}/%{_bindir}/gzip %{buildroot}/%{_bindir}/../../bin/

%files
%license COPYING
%{_bindir}/*
%{_bindir}/../../bin/gzip
%doc %{_infodir}/*.info*.gz
%doc %{_mandir}/man1/*.gz

%changelog