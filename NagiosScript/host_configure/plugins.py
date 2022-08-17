from subprocess import run
from typing import Final


BASH: Final = "/bin/bash"


def install():
    run(
        "sudo apt-get install -y autoconf gcc libc6 libmcrypt-dev make libssl-dev wget bc gawk dc build-essential snmp libnet-snmp-perl gettext",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )

    run(
        "cd /tmp ; wget --no-check-certificate -O nagios-plugins.tar.gz https://github.com/nagios-plugins/nagios-plugins/archive/release-2.2.1.tar.gz ; tar zxf nagios-plugins.tar.gz",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )
    run(
        "cd /tmp/nagios-plugins-release-2.2.1/ ; sudo ./tools/setup ; sudo ./configure ; sudo make ; sudo make install",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )
    run(
        "/usr/local/nagios/libexec/check_nrpe -H 127.0.0.1 -c check_load",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )
