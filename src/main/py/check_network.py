#!/usr/bin/env python

from os import system
from sensors_functions import iso_timestamp
from time import sleep


def wifi_test():
    system("ping -c 1 192.168.1.3 | grep \" bytes from \"")
    system("ping -c 1 192.168.1.1 | grep \" bytes from \"")
    system("ping -c 1 www.free.fr | grep \" bytes from \"")
    system("sudo iwlist wlp2s0 scan | grep 'Quality=\\|ESSID:\\|Address:\\|Frequency:'")
    return True


def main():  # Expected to be launched at startup
    print(iso_timestamp() + " - Starting network test...")
    successful_tests = 0
    failed_tests = 0
    failures_in_a_row = 0
    while True:
        if wifi_test():
            successful_tests = successful_tests + 1
            failures_in_a_row = 0
        else:
            failed_tests = failed_tests + 1
            failures_in_a_row = failures_in_a_row + 1
        sleep(59)


if __name__ == "__main__":
    main()
