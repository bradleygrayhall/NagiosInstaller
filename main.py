import os
from configGenerator import *
from typing import Final
NAGIOS_PATH: Final = 'nagios.cfg'

def enable_cfg_file(name):
    cfgName = name + ".cfg\n"
    filePath = "cfg_file=/usr/local/nagios/etc/objects/" + cfgName
    os.chdir('/usr/local/nagios/etc')
    f1= open(NAGIOS_PATH, 'r')
    f2 = open('temp.cfg', 'w')
    for line in f1:
        f2.write(line.replace('#'+filePath, filePath))
    f1.close()
    f2.close()
    os.remove(NAGIOS_PATH)
    os.rename('temp.cfg',NAGIOS_PATH)
    ###TODO: write object class that will gen config files for nagios




def create_switch_config():
    count = 0
    switch_names = []
    ips=[]
    host_names=[]
    services = [[]]
    #enable_cfg_file("switch")
    while True:
        os.system('clear')
        print("We will now allow you to input all your switches info before we design the config file for you!\n\n")
        switch_names.append(input("Please input the name of your switch; if you are done type in 'Q':"))
        if switch_names[count].upper() == 'Q':
            os.system('clear')
            print("\n")
            break
        else:
            os.system('clear')
            ips.append(input("Please input the ip of the switch:\n"))
            host_names.append(input("Please input the host name of the switch"))
            count += 1
            os.system('clear')
    for i in range(len(ips)):
        count = 0
        temp = []
        while True:
            temp.append(input("Please specify what services you'd like to use. Press Q when done: "))
            if temp[count].upper() == 'Q':
                del temp[count]
                services.append(temp)
                break
            else:
                count += 1
                os.system('clear')
    ###TODO: add code to check for q, and then loop through double list
    switch(switch_names, ips, host_names)
    service(services,host_names)
    ####TODO: add code for service definitions and host definitions
    ####TODO: pass group of code to config-gen function

def make_install(word):
    os.system('sudo make install' + word)


def a2enmod(word):
    os.system('sudo a2enmod' + word)

def ufw(word):
    os.system('sudo ufw ' + word)

def install_nagios():
    os.system('clear')
    os.system('wget -O Nagios.tar.gz https://github.com/NagiosEnterprises/nagioscore/archive/nagios-4.4.6.tar.gz')
    os.system('wget --no-check-certificate -O Plugins.tar.gz https://github.com/nagios-plugins/nagios-plugins/archive/release-2.3.3.tar.gz')
    os.system('tar xzf Nagios.tar.gz')
    os.system('tar zxf Plugins.tar.gz')
    os.mkdir('Nagios')
    os.mkdir('Plugins')
    os.system('mv nagioscore*/* Nagios')
    os.system('rm -rf nagioscore*')
    os.system('mv nagios*/* Plugins')
    os.system('rm -rf nagios*')
    os.chdir('Nagios')
    os.system('./configure --with-httpd-conf=/etc/apache2/sites-enabled')
    os.system('sudo make all')
    os.system('sudo make install-groups-users')
    os.system('sudo usermod -a -G nagios www-data')
    make_install('')
    make_install('-daemoninit')
    make_install('-commandmode')
    make_install('-config')
    make_install('-webconf')
    a2enmod(' rewrite')
    a2enmod(' cgi')
    ufw('allow Apache')
    ufw('reload')
    os.system('sudo htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin')
    os.system('sudo systemctl restart apache2.service')
    os.system('sudo systemctl start nagios.service')
    os.chdir('..')
    os.chdir('Plugins')
    os.system('./tools/setup')
    os.system('./configure')
    os.system('sudo make')
    make_install('')
    os.system('sudo systemctl restart nagios.service')


def create_host_config():
    pass


def main():
    user = input("Is this the server? (y/n)")
    if user == "n":
        user = input("Is this a host? (y/n)")
        if user == "n":
            create_switch_config()
        elif user == "y":
            create_host_config()
        else:
            print("You drunk?")
    elif user == "y":
        install_nagios()
    else:
        print("You drunk?")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/