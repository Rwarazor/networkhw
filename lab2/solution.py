import argparse
import ipaddress
import re
import platform
import subprocess


def is_valid_ipaddress(address):
    try:
        ipaddress.ip_address(address)
        return True
    except:
        return False


# source: https://stackoverflow.com/questions/2532053/validate-a-hostname-string
def is_valid_hostname(hostname):
    if hostname[-1] == ".":
        # strip exactly one dot from the right, if present
        hostname = hostname[:-1]
    if len(hostname) > 253:
        return False

    labels = hostname.split(".")

    # the TLD must be not all-numeric
    if re.match(r"[0-9]+$", labels[-1]):
        return False

    allowed = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(label) for label in labels)


def ping(args, size):
    command = ["ping", args.hostname]
    match platform.system().lower():
        case "windows":
            command += ["-f", "-n", "1", "-l", str(size)]
        case "darwin":
            command += ["-D", "-c", "1", "-s", str(size)]
        case _:
            command += ["-M", "do", "-c", "1", "-s", str(size)]
    #print(command)

    for i in range(args.count):
        if subprocess.call(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) == 0:
            return True
        elif i + 1 != args.count and args.verbose:
            print(f"Host {args.hostname} was not reached, trying again", flush=True)
    return False


MIN_MTU = 68
MAX_MTU = 1500

PING_PACKET_SIZE = 28

def find_mtu(args):
    if not ping(args, 0):
        print(f"{args.hostname} is unreachable")
        exit(1)

    l = MIN_MTU
    r = MAX_MTU + 1
    while r - l > 1:
        m = (l + r) // 2
        if ping(args, m - PING_PACKET_SIZE):
            l = m
            if args.verbose:
                print(f"MTU >= {l}", flush=True)
        else:
            r = m
            if args.verbose:
                print(f"MTU < {r}", flush=True)
    return l


def main():
    parser = argparse.ArgumentParser(
        "MTUFinder",
        "./MTUFinder <hostname>"
    )
    parser.add_argument("hostname")
    parser.add_argument("--count", "-c", default=3, type=int, help="Number of packets > 0, host is \
                        considered reachable if at least one packet reaches.")
    parser.add_argument("--verbose", "-v", action='store_true', help="Enable aditional output")
    args = parser.parse_args()

    if args.count <= 0:
        print(f"--count must be positive, value given: {args.count}")

    if not is_valid_ipaddress(args.hostname) and not is_valid_hostname(args.hostname):
        print(f"<hostname> must be a valid hostname, value given: {args.hostname}")
        exit(1)
    mtu = find_mtu(args)
    print(f"MTU to {args.hostname} is {mtu}")


if __name__ == '__main__':
    main()