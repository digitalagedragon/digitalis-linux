#!/bin/bash

set -e
set -x

mkdir -pv repo
cp -ru bootstrap-repo/distfiles repo/

make

rm -fv targetdir_1/var/db/x10/installed
# x10/x10 -config ./etc/x10.bootstrap3.conf:./etc/x10.nodeps.conf build -maybe -with_deps pkgs/sys-libs/glibc.yml
# x10/x10 -config ./etc/x10.bootstrap3.conf:./etc/x10.nodeps.conf install sys-libs/glibc targetdir_1

# X10_DEBUG=1 x10/x10 --repo repo \
#         --packages pkgs \
#         --no-use-generated \
#         build python/libxml2 \
#         --target-root targetdir_1 \
#         --no-reset \
#         --force

x10/x10 --repo repo \
        --packages pkgs \
        --no-use-generated \
        build virtual/base-minimal \
        --target-root targetdir_1 \
        --no-reset \
        --force

uuid=$(uuidgen)
mkdir -p /tmp/x10/targetdir.$uuid
function cleanup {
    rm -rf /tmp/x10/targetdir.$uuid
}
trap cleanup EXIT

mkdir -p /tmp/x10/targetdir.$uuid/var/db/x10/
cp targetdir_1/var/db/x10/pkgdb.yml /tmp/x10/targetdir.$uuid/var/db/x10/

x10/x10 --repo repo --packages pkgs install virtual/base-minimal /tmp/x10/targetdir.$uuid

rm -rf targetdir
mv /tmp/x10/targetdir.$uuid targetdir
