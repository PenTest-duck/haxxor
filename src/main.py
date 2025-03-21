import subprocess
import time
import argparse
from hacker.hacker import Hacker

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=str, help="The target IP address")
    args = parser.parse_args()

    print("Setting up OpenVPN connection...")
    subprocess.Popen(["openvpn", "--config", "/app/connections/htb.ovpn"])
    time.sleep(5) # Give OpenVPN 5 seconds to set up
    print("OpenVPN connection should be established.")

    hacker = Hacker()
    hacker.run(args.target)


if __name__ == "__main__":
    main()
