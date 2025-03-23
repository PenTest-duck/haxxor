import psutil
import shutil
import subprocess
import os
import argparse

from logger import get_logger
from constants import DEFAULT_MODEL, DEFAULT_MODEL_PROVIDER

logger = get_logger(__name__)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=str, required=True, help="The target IP address")
    parser.add_argument("--connection", type=str, required=False, help="The name of the OpenVPN connection to use", default="lab")
    parser.add_argument("--model", type=str, required=False, help="The name of the LLM model to use", default=f"{DEFAULT_MODEL_PROVIDER}:{DEFAULT_MODEL}")
    parser.add_argument("--name", type=str, required=False, help="The name of the target machine", default="")
    return parser.parse_args()

def test_connection(target: str) -> bool:
    try:
        subprocess.run(["ping", "-c", "1", target], check=True, stdout=subprocess.DEVNULL)
        logger.info("Target is reachable through ping.")
        return True
    except subprocess.CalledProcessError:
        logger.error(f"Could not ping target {target}. Exiting.")
    return False

def is_openvpn_running():
    for process in psutil.process_iter(attrs=["name"]):
        if process.info["name"] == "openvpn":
            return True
    return False

def setup_openvpn_connection(connection: str):
    if is_openvpn_running():
        logger.info("OpenVPN process seems to be running already. No need to open a new connection.")
    else:
        logger.info("Setting up OpenVPN connection...")
        process = subprocess.Popen(
            ["openvpn", "--config", f"/app/connections/{connection}.ovpn"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        for line in iter(process.stdout.readline, ""):
            logger.debug(f"OpenVPN: {line.strip()}")
            if "Protocol options: explicit-exit-notify 1" in line:
                logger.info("OpenVPN connection established")
                break

def setup_workspace_dir(target: str):
    workspace_dir = f"/tmp/{target}"
    if os.path.exists(workspace_dir):
        logger.info(f"Workspace directory already exists at {workspace_dir}. Deleting its contents.")
        shutil.rmtree(workspace_dir)
    
    os.mkdir(workspace_dir)
    logger.info(f"Created workspace directory at {workspace_dir}")

def setup(target: str, connection: str):
    setup_openvpn_connection(connection)
    setup_workspace_dir(target)
