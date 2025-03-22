import subprocess
from hacker.hacker import HackerAgent
from utils import parse_args, setup
from logger import get_logger

logger = get_logger(__name__)

def hack_target(target: str) -> str | None:
    try:
        subprocess.run(["ping", "-c", "1", target], check=True, stdout=subprocess.DEVNULL)
        logger.info("Target is reachable through ping.")
    except subprocess.CalledProcessError:
        logger.error(f"Could not ping target {target}. Exiting.")
        return None

    hacker = HackerAgent()

    try:
        flag = hacker.run(target)
    except Exception as e:
        logger.error(f"Exiting gracefully due to error: {e}")
        logger.info("\nShutting down OpenVPN connection...")
        subprocess.run(["pkill", "-f", "openvpn"])
        logger.info("OpenVPN connection terminated.")
        return None
    
    if flag:
        logger.info(f"Flag found: {flag}")
    else:
        logger.info("No flag found.")
    return flag

def main():
    args = parse_args()
    setup(args.target, args.connection)

    flag = hack_target(args.target)
    if flag:
        logger.info("✅ YAY! We did it! 🎉")

if __name__ == "__main__":
    main()
