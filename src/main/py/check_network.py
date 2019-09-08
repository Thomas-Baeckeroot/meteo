#!/usr/bin/env python

from os import system
from utils import iso_timestamp_now
from time import sleep


def log_ping(host):
    rc = system("ping -c 1 " + host + " | grep \" bytes from \"")
    if rc != 0:
        print("ERROR! Ping to " + host + " failed with return code " + str(rc) + ".")
    return rc


def wifi_test():
    system("sudo iwlist wlp2s0 scan | grep 'Quality=\\|ESSID:\\|Address:\\|Frequency:'")
    log_ping("192.168.1.3")
    log_ping("192.168.1.1")
    if log_ping("www.free.fr") != 0:
        # print("Ping to internet FAILED. Raspberry should change network (SSID/antenna) here...")
        return False
    return True


def main():  # Expected to be launched at startup
    print(iso_timestamp_now() + " - Starting network test...")
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
