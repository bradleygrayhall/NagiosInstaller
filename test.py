import re

with open("commands.cfg", "r") as file:
    content = file.read()
    strang = "define command{\n\n\tcommand_name\t\tcheck_nrpe\n\tcommand_line\t\t$USER1$/check_nrpe -H $HOSTADDRESS$ -c $ARG1$\n}\n"
print(type(content))
if content.find(strang):
    file.close()
else:
    file.open()
