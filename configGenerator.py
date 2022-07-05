def services(services,host_names):
    config = open('switch.cfg', 'a')
    string_build = ""
    for i in range(0, len(services)):
        for j in range(0, len(services[i])):
            string_build = "define host {\n"
            string_build += "\tuse\t\tSwitches\n"
            string_build += "\thost_name\t" + host_names[i] + "\n" + "\tservice_description\t" + services[j].upper()
            #string_build +=

            #string_build +=

def switch(switch_names, ips, host_names):
    config = open('switch.cfg', 'a')
    string_build = ""
    for i in range(0, len(switch_names)-1):
        string_build = "define host {\n"
        string_build += "\tuse\t\tSwitches\n"
        string_build += "\thost_name\t" + host_names[i] + "\n" + "'\talias\t" + switch_names[i] + " Switch\n"
        string_build += "\taddress\t" + ips[i] + "\n" + "\thostgroups\t" + "allhosts,switches\n"
        string_build += "}\n\n"
        config.write(string_build)
        string_build = ""
    config.close()


def host():
    pass
