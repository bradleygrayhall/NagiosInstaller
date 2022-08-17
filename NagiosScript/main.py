from prettyify import clear_Terminal
from installNagios import install
from nagiosHost import configure_host
from nagiosSwitch import configure_switch


def main():
    while 1:
        print("-------------------------------------------------")
        print("Type 1. if you want to install Nagios")
        print("Type 2. if you want to configure host.cfg")
        print("Type 3. if you want to configure switch.cfg")
        print("Type q. if you want to exit the program")
        print("-------------------------------------------------\n\n")
        choice = input("input selection here: ")
        clear_Terminal()
        if choice == "1":
            install()
        elif choice == "2":
            configure_host()
        elif choice == "3":
            configure_switch()
        elif choice.capitalize() == "Q":
            break
        else:
            print("This is not a valid input")
        clear_Terminal()


if __name__ == "__main__":
    main()
