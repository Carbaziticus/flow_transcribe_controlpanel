#! python3

# SysInfo.py
import platform
import subprocess


def system():
    system = platform.system()
    # print(system)
    return(system)


def release():
    release = platform.release()
    # print(release)
    return(release)


def macAddress():
    if system() == 'Darwin':
        cmd = "ifconfig en0 | grep 'ether' | awk '{print $2}'"
        result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, check=True)
        result = result.stdout.strip()  # eth0 MAC address
        mac_address = result.decode('UTF8')
        print("en0 MAC address:", mac_address)
        mac_clean = mac_address.replace(':', '')
    elif system() == 'Windows':
        cmd = "ipconfig /all | find \"Physical Address\""
        result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, check=True)
        result = result.stdout.strip()
        mac_address = result.decode('UTF8')
        mac_address = mac_address.split(': ')
        # a currently connected ethernet hardware interface address
        mac_address = mac_address[1]
        print("currently active MAC address:", mac_address)
        mac_clean = mac_address.replace('-', '')
    return(mac_clean)
