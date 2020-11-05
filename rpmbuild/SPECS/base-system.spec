Name:     base-system
Version:  2
Release:  1%{?dist}
Summary:  Virtual package for basic system setup
BuildArch: noarch

License:  None

Requires: fs-tree

Requires: bash
Requires: coreutils
Requires: diffutils
Requires: file
Requires: findutils
Requires: gawk
Requires: grep
Requires: gzip
Requires: pkg-config
Requires: sed
Requires: shadow
Requires: tzdata
Requires: util-linux
Requires: which

Requires: dnf
Requires: digitalis-repository

BuildRequires: /usr/bin/true

%description

%files

%changelog

- 2020-11-04 Morgan Thomas <m@m0rg.dev>
  Added util-linux to requires, version -> 2