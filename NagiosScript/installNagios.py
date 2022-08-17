from subprocess import run

try:
    from os import chdir, uname
except:
    from os import chdir
from typing import Final

# CONSTANTS
BASH: Final = "/bin/bash"


def install():
    if uname()[3].find("Ubuntu"):
        run(
            "sudo apt-get update",
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            executable=BASH,
        )
        run(
            "sudo apt-get install -y autoconf gcc libc6 make wget unzip apache2 php libapache2-mod-php7.4 libgd-dev",
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            executable=BASH,
        )
        run(
            "sudo apt-get install openssl libssl-dev",
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            executable=BASH,
        )
    elif uname()[3].find("Centos"):
        pass
    chdir("/tmp")
    run(
        "wget -O nagioscore.tar.gz https://github.com/NagiosEnterprises/nagioscore/archive/nagios-4.4.6.tar.gz ; tar xzf nagioscore.tar.gz ",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )
    chdir("/tmp/nagioscore-nagios-4.4.6")
    run(
        "sudo ./configure --with-httpd-conf=/etc/apache2/sites-enabled ; sudo make all; sudo make install-groups-users; sudo usermod -a -G nagios www-data ; sudo make install",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )
    run(
        "sudo make install-daemoninit ; sudo make install-commandmode ; sudo make install-config ; sudo make install-webconf ; sudo a2enmod rewrite ; sudo a2enmod cgi",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )
    run(
        "sudo ufw allow Apache ; sudo ufw reload ; sudo htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin ; sudo systemctl start nagios.service ; sudo systemctl restart apache2.service",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )
    if uname()[3].find("Ubuntu"):
        run(
            "sudo apt-get install -y autoconf gcc libc6 libmcrypt-dev make libssl-dev wget bc gawk dc build-essential snmp libnet-snmp-perl gettext ; cd /tmp",
            shell=True,
            stdin=None,
            stderr=None,
            executable=BASH,
        )
    elif uname()[3].find("Centos"):
        pass
    chdir("../")
    run(
        "wget --no-check-certificate -O nagios-plugins.tar.gz https://github.com/nagios-plugins/nagios-plugins/archive/release-2.3.3.tar.gz ; tar xzf nagios-plugins.tar.gz",
        shell=True,
        stdin=None,
        stderr=None,
        executable=BASH,
    )
    chdir("/tmp/nagios-plugins-release-2.3.3/")
    run(
        "sudo ./tools/setup ; sudo ./configure ; sudo make ; sudo make install ; sudo systemctl restart nagios.service",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )
