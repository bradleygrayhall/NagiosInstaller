import os
from subprocess import call


def clear_Terminal():
    call("clear" if os.name == "posix" else "cls")
