import subprocess
from typing import Optional
from hacker.hacker import HackerAgent
from utils import parse_args, setup, test_connection
from logger import get_logger

logger = get_logger(__name__)

def hack_target(target: str, model: str, name: Optional[str]) -> str | None:
    if not name:
        name = target
    if not test_connection(target):
        return None
    
    hacker = HackerAgent(model)

    try:
        result = hacker.run(target, name)
    except Exception as e:
        logger.error(f"Exiting gracefully due to error: {e}")
        logger.info("\nShutting down OpenVPN connection...")
        subprocess.run(["pkill", "-f", "openvpn"])
        logger.info("OpenVPN connection terminated.")
        return None
    
    if result.success:
        logger.info(f"Flag found: {result.flag}")
    else:
        logger.info("No flag found.")
    return result.flag

def main():
    args = parse_args()
    setup(args.target, args.connection)

    flag = hack_target(args.target, args.model, args.name)
    if flag:
        logger.info("✅ YAY! We did it! 🎉")

if __name__ == "__main__":
    main()
