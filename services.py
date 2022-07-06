def check(service):
    temp = "\n\tservice_description\t\t"
    if service.upper() == "PING":
        temp += "PING\n\t"
        temp += "check_ping!200.0,20%!600.0,60%\n" + "\tnormal_check_interval\t5\n"
        temp += "\tretry_check_interval\t1\n"
    elif service.upper() == "SNMP":
        temp += "Uptime and link status\n\t"
        temp += "check_command\t\tcheck_snmp!-C public -o sysUpTime.0\n"
        temp += "\tcheck_command\t\tcheck_snmp!-C public -o "
        for i in range(1, 25):
            temp += "ifOperStatus.{} -r 1 -m RFC1213-MIB, -o ".format(i)
    else:
        return ""
    return temp