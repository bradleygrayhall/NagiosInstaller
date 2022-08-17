import os
from subprocess import run
from prettyify import clear_Terminal
from installNagios import BASH
import csv


def add_nrpe_to_nagios():
    pass


def add_server_folder_to_nagios_config():
    pass


def write_host_from_csv():
    clear_Terminal()
    csvreader = csv.reader(open("Hosts.csv"))
    rows = []
    for row in csvreader:
        rows.append(row)
    os.mkdir("Windows-cfg")
    os.mkdir("Unix-cfg")
    str_build = ""
    for row in rows:
        if row[1] != "Host":
            if row[2].upper() == "NO":
                os.chdir("Unix-cfg")
                file = open(f"{row[1]}.cfg", "w")
                str_build += f"define host{{\n\tuse\t\tlinux-server\n\thost_name\t\t{row[1]}\n\talias\t\t{row[1]}\n\taddress\t\t{row[0]}\n}}\n\n"
                str_build += f"define service{{\n\tuse\t\tgeneric-service\n\thost_name\t\t{row[1]}\n\tservice_description\t\tCPU_Load\n\tcheck_command\t\tcheck_nrpe!check_load}}"
                file.write(str_build)
                file.close()
                os.chdir("..")
                str_build = ""
            elif row[2].upper() == "YES":
                os.chdir("Windows-cfg")
                file = open(f"{row[1]}.cfg", "w")
                file.close()


def write_host_single():
    str_build = ""
    file = open("free-willy-tester.cfg", "w")
    str_build += "define host{\n\tuse\t\tlinux-server\n\thost_name\t\tfree-willy-tester\n\talias\t\tfree-willy-tester\n\taddress\t\t172.18.16.255\n}\n\n"
    str_build += "define service{\n\tuse\t\tGeneric-Service\n\thost_name\t\tfree-willy-tester\n\tservice_description\t\tPING\n\tcheck_command\t\tcheck_nrpe!check_ping!100.0,20%!500.0,60%\n\tnotifications_enabled\t\t1\n\tprocess_perf_data\t\t1\n}"
    file.write(str_build)
    file.close()
    run(
        "sudo mv free-willy-tester.cfg /usr/local/nagios/etc/servers/",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )


def configure_host():
    clear_Terminal()
    run(
        "cd /tmp ; wget --no-check-certificate -O nrpe.tar.gz https://github.com/NagiosEnterprises/nrpe/archive/nrpe-4.0.3.tar.gz ; tar xzf nrpe.tar.gz",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )
    run(
        "cd /tmp/nrpe-nrpe-4.0.3/ ; sudo ./configure --enable-command-args --with-ssl-lib=/usr/lib/x86_64-linux-gnu/ ; sudo make all ; sudo make install-plugin",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )
    add_nrpe_to_nagios()
    add_server_folder_to_nagios_config()
    temp = input("")
    clear_Terminal()
    if temp.capitalize() is "D":
        write_host_single()
    else:
        write_host_from_csv()
    try:
        os.chdir("/usr/local/nagios/etc/servers")
    except:
        run(
            "sudo mkdir /usr/local/nagios/etc/servers",
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            executable=BASH,
        )
