from subprocess import run
from os import chdir, remove, rename
from typing import Final
from installNagios import BASH
from pathlib import Path
from services import check
from prettyify import clear_Terminal

NAGIOS_CFG: Final = "nagios.cfg"


def service(services, host_names):
    config = open("switch.cfg", "a")
    string_build = ""
    for i in range(0, len(services)):
        for j in range(0, len(services[i])):
            string_build = "define service {\n"
            string_build += "\tuse\t\tSwitches\n"
            string_build += "\thost_name\t" + host_names[i - 1]
            string_build += check(services[i][j])
            string_build += "\n}\n\n"
            config.write(string_build)
        string_build = ""
    config.close()


def switch(switch_names, ips, host_names):
    config = open("switch.cfg", "a")
    string_build = ""
    for i in range(0, len(switch_names) - 1):
        string_build = "define host {\n"
        string_build += "\tuse\t\tSwitches\n"
        string_build += (
            "\thost_name\t"
            + host_names[i]
            + "\n"
            + "\talias\t"
            + switch_names[i]
            + " Switch\n"
        )
        string_build += (
            "\taddress\t" + ips[i] + "\n" + "\thostgroups\t" + "allhosts,switches\n"
        )
        string_build += "}\n\n"
        config.write(string_build)
        string_build = ""
    config.close()


def enable_cfg(name):
    lookForLine = f"cfg_file=/usr/local/nagios/etc/objects/{name}.cfg"
    f1 = open(NAGIOS_CFG, "r")
    f2 = open("temp.cfg", "w")
    for line in f1:
        f2.write(line.replace(f"#{lookForLine}", lookForLine))
    f1.close()
    f2.close()
    remove(NAGIOS_CFG)
    rename("temp.cfg", NAGIOS_CFG)
    run(
        f"sudo mv nagios.cfg /usr/local/nagios/etc/nagios.cfg",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )


def add_services_to_monitor():
    count = 0
    switch_names = []
    ips = []
    host_names = []
    services = []
    while True:
        clear_Terminal()
        print("Time to input your switch info")
        switch_names.append(
            input(
                "Input the name of your switch; if you are done inputing switches type in 'Q': "
            )
        )
        if switch_names[count].upper() == "Q":
            clear_Terminal()
            print("\n")
            break
        else:
            clear_Terminal()
            ips.append(input("Please input the ip of the switch: "))
            host_names.append(input("Please input the host name of the switch: "))
            count += 1
            clear_Terminal()
    for i in range(len(ips)):
        count = 0
        temp = []
        while True:
            temp.append(
                input(
                    "Please specify what services you'd like to use. Press Q when done: "
                )
            )
            if temp[count].upper() == "Q":
                del temp[count]
                services.append(temp)
                break
            else:
                count += 1
                clear_Terminal()
    switch(switch_names, ips, host_names)
    service(services, host_names)


def configure_switch():
    home = str(Path.home())
    chdir("/usr/local/nagios/etc/")
    run(
        f"sudo cp -r nagios.cfg {home}/NagiosScript/nagios.cfg",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )
    chdir(f"{home}/NagiosScript")
    enable_cfg("switch")
    add_services_to_monitor()
    run(
        f"sudo mv {home}/NagiosScript/switch.cfg /usr/local/nagios/etc/objects/switch.cfg ; /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg ; /etc/rc.d/init.d/nagios reload",
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        executable=BASH,
    )
