def check(service):
    temp = "\n\tservice_description\t\t"
    if service.upper() == "PING":
        temp += "PING\n\t"
        temp += "check_ping!200.0,20%!600.0,60%\n" + "\tnormal_check_interval\t5\n"
        temp += "\tretry_check_interval\t1\n"
    elif service.upper() == "SNMP":
        temp += "Uptime and link status\n\t"
        temp += "check_command\t\tcheck_snmp!-C public -o sysUpTime.0\n"
        for i in range(0, 24)
        temp += "check_command\t\tcheck_snmp!-C public -o ifOper.{i}"
    elif service.upper() == ""