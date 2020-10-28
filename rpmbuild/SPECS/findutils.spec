Name:           findutils
Version:        4.7.0
Release:        1%{?dist}
Summary:        The GNU Find Utilities are the basic directory searching utilities of the GNU operating system.

License:        GPLv3+
URL:            https://www.gnu.org/software/findutils
%undefine       _disable_source_fetch
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
%define         SHA256SUM0 c5fefbdf9858f7e4feb86f036e1247a54c79fc2d8e4b7064d5aaa1f47dfa789a

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
mv -v %{buildroot}/%{_bindir}/find %{buildroot}/%{_bindir}/../../bin/
sed -i 's|find:=\${BINDIR}|find:=/bin|' %{buildroot}/%{_bindir}/updatedb

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%{_bindir}/*
%{_bindir}/../../bin/find
%{_libexecdir}/frcode
%doc %{_infodir}/*.info*.gz
%doc %{_mandir}/man1/*.gz
%doc %{_mandir}/man5/*.gz

%changelog