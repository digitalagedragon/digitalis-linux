Name:           podman
Version:        2.0.6
Release:        3%{?dist}
Summary:        OCI container management tool

License:        Apache-2.0
URL:            https://podman.io
%undefine       _disable_source_fetch
Source0:        https://github.com/containers/libpod/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%define         SHA256SUM0 990c341fe563d34a25ebab818af60480061cb80e4e8d61eacbdeb998151d6663

%if "%{_build}" != "%{_host}"
%error This package is not set up for cross-compilation.
%endif

BuildRequires:  libassuan-devel
BuildRequires:  glib2-devel
BuildRequires:  libgpgme-devel
BuildRequires:  libseccomp-devel
BuildRequires:  libdevice-mapper-devel
BuildRequires:  golang
BuildRequires:  make
BuildRequires:  git

Requires:       containers-common
Requires:       runc
Requires:       cni-plugins
Requires:       conmon
Requires:		/usr/sbin/iptables

%undefine _annotated_build
%define debug_package %{nil}

%description

%prep
echo "%SHA256SUM0  %SOURCE0" | sha256sum -c -
%autosetup

%build
mkdir _build
pushd _build
mkdir -p src/github.com/containers/v2
ln -s $(dirs +1 -l) src/github.com/containers/v2/libpod
popd

mv vendor src
export GOPATH=$PWD/_build:$PWD
export BUILDTAGS='seccomp apparmor containers_image_ostree_stub btrfs_noversion exclude_graphdriver_btrfs'

go build -buildmode pie -compiler gc -tags="$BUILDTAGS" -o bin/podman github.com/containers/libpod/v2/cmd/podman

%install
export GOPATH=$PWD/_build:$PWD

%{__install} -D -m0755 bin/podman %{buildroot}%{_bindir}/podman
%{__install} -m 644 -D completions/bash/podman %{buildroot}%{_datadir}/bash-completion/completions/podman
%{__install} -m 644 -D completions/zsh/_podman %{buildroot}%{_datadir}/zsh/site-functions/_podman
%{__install} -dm755 %{buildroot}%{_sysconfdir}/cni/net.d
%{__install} -m644 cni/87-podman-bridge.conflist %{buildroot}%{_sysconfdir}/cni/net.d/

# from Void's package
sed -e 's|# cgroup_manager = "systemd"|cgroup_manager = "cgroupfs"|g' \
		src/github.com/containers/common/pkg/config/containers.conf \
		>containers.cgfs.conf
%{__install} -m644 -D containers.cgfs.conf %{buildroot}%{_datadir}/containers/containers.conf

%files
%license LICENSE
%{_bindir}/podman
%{_sysconfdir}/cni/net.d/87-podman-bridge.conflist
%{_datadir}/containers/containers.conf
%{_datadir}/bash-completion/completions/*
%{_datadir}/zsh/site-functions/*
%doc README.md

%changelog