from os import chdir, name, uname
from subprocess import run
from typing import Final
from pathlib import Path
from plugins import install

# CONSTANTS
BASH: Final = "/bin/bash"
NRPE: Final = "nrpe.cfg"
HOME: Final = str(Path.home())


def main():
    if name == "posix":
        if uname()[3].find("Ubuntu"):
            run(
                "sudo apt-get update ; sudo apt-get install -y autoconf automake gcc libc6 libmcrypt-dev make libssl-dev wget openssl",
                shell=True,
                stdin=None,
                stdout=None,
                stderr=None,
                executable=BASH,
            )
        elif uname()[3].find("Centos"):
            pass
        run(
            "cd /tmp ; wget --no-check-certificate -O nrpe.tar.gz https://github.com/NagiosEnterprises/nrpe/archive/nrpe-4.0.3.tar.gz ; tar xzf nrpe.tar.gz",
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            executable=BASH,
        )
        run(
            "cd /tmp/nrpe-nrpe-4.0.3/ ; sudo ./configure --enable-command-args --with-ssl-lib=/usr/lib/x86_64-linux-gnu/ ; sudo make all",
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            executable=BASH,
        )
        chdir("/tmp/nrpe-nrpe-4.0.3")
        run(
            "sudo make install-groups-users ; sudo make install ; sudo make install-config",
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            executable=BASH,
        )

        run(
            'sudo sh -c "echo >> /etc/services" ; sudo sh -c "sudo echo \'# Nagios services\' >> /etc/services" ; sudo sh -c "sudo echo \'nrpe    5666/tcp\' >> /etc/services"',
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            executable=BASH,
        )
        run(
            "sudo make install-init ; sudo systemctl enable nrpe.service",
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            executable=BASH,
        )
        run(
            "sudo mkdir -p /etc/ufw/applications.d ; sudo sh -c \"echo '[NRPE]' > /etc/ufw/applications.d/nagios\" ; sudo sh -c \"echo 'title=Nagios Remote Plugin Executor' >> /etc/ufw/applications.d/nagios\" ; sudo sh -c \"echo 'description=Allows remote execution of Nagios plugins' >> /etc/ufw/applications.d/nagios\" ; sudo sh -c \"echo 'ports=5666/tcp' >> /etc/ufw/applications.d/nagios\" ; sudo ufw allow NRPE ; sudo ufw reload",
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            executable=BASH,
        )
        run(
            f"sudo cp -r /usr/local/nagios/etc/{NRPE} {HOME}/host_configure",
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            executable=BASH,
        )
        host = input("Please input the ip of the server that is monitoring this host: ")
        run(
            f"""sudo sh -c "sed -i '/^allowed_hosts=/s/$/,{host}/' /usr/local/nagios/etc/nrpe.cfg" ; sudo sh -c "sed -i 's/^dont_blame_nrpe=.*/dont_blame_nrpe=1/g' /usr/local/nagios/etc/nrpe.cfg" """,
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            executable=BASH,
        )
        run(
            "sudo systemctl start nrpe.service ; /usr/local/nagios/libexec/check_nrpe -H 127.0.0.1",
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            executable=BASH,
        )
        install()
    else:
        pass


main()
