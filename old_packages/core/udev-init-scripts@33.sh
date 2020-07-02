export VERSION=33

export RDEPEND="core/eudev"

pkg_build() {
    mkdir -p etc/init.d/
    cat > etc/init.d/udev << "EOF"
#!/sbin/openrc-run
# Copyright 1999-2013 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

command_args="${udev_opts}"
command_background=yes
pidfile=/run/udev.pid
description="udev manages device permissions and symbolic links in /dev"
extra_started_commands="reload"
description_reload="Reload the udev rules and databases"

depend()
{
        need sysfs dev-mount
        before checkfs fsck
        keyword -lxc -systemd-nspawn -vserver
}

get_udevd_binary() {
        local bins="/sbin/udevd /lib/systemd/systemd-udevd /usr/lib/systemd/systemd-udevd"
        for f in ${bins}; do
                if [ -x "$f" -a ! -L "$f" ]; then
                        command="$f"
                fi
        done
        if [ -z "$command" ]; then
                eerror "Unable to find udev executable."
                return 1
        fi
}

start_pre()
{
        # make sure devtmpfs is in the kernel
        if ! grep -qs devtmpfs /proc/filesystems; then
                eerror "CONFIG_DEVTMPFS=y is required in your kernel configuration"
                eerror "for this version of udev to run successfully."
                eerror "This requires immediate attention."
                if ! mountinfo -q /dev; then
                        mount -n -t tmpfs dev /dev
                        busybox mdev -s
                        mkdir /dev/pts
                fi
                return 1
        fi

        # make sure /dev is a mounted devtmpfs
        if ! mountinfo -q -f devtmpfs /dev; then
                eerror "Udev requires /dev to be a mounted devtmpfs."
                eerror "Please reconfigure your system."
                return 1
        fi

        # load unix domain sockets if built as module, Bug #221253
        # and not yet loaded, Bug #363549
        if [ ! -e /proc/net/unix ]; then
                if ! modprobe unix; then
                        eerror "Cannot load the unix domain socket module"
                        return 1
                fi
        fi

        get_udevd_binary || return 1

        if [ -e /proc/sys/kernel/hotplug ]; then
                echo "" >/proc/sys/kernel/hotplug
        fi

        if yesno "${udev_debug:-NO}"; then
                command_args="${command_args} --debug 2> /run/udevdebug.log"
        fi

        return 0
}

stop()
{
        local rc=0
        ebegin "Stopping ${name:-$RC_SVCNAME}"
        udevadm control --exit
        rc=$?
        if [ $rc -ne 0 ]; then
                eend $rc "Failed to stop $RC_SVCNAME using udevadm"
                ebegin "Trying with start-stop-daemon"
                start-stop-daemon --stop --pidfile "${pidfile}"
                rc=$?
        fi
        [ $rc -eq 0 ] && rm -f "${pidfile}"
        eend $rc "Failed to stop $RC_SVCNAME"
}

reload()
{
        ebegin "reloading udev rules and databases"
        udevadm control --reload
        eend $?
}
EOF
    chmod +x etc/init.d/udev
    mkdir -p etc/runlevels/sysinit/
    ln -s /etc/init.d/udev etc/runlevels/sysinit/udev
}