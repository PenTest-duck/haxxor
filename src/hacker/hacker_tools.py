from langchain_core.tools import tool
import subprocess

@tool
def run_command(command: str) -> str:
    """Run a shell command."""
    try:
        result = subprocess.run(command, capture_output=True, shell=True, text=True)
    except FileNotFoundError:
        cmd = command.split()[0]
        return f"Command not found: {cmd}"
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        return f"Command failed with the following error:\n{e.stderr}"
    
    return result.stdout

@tool
def run_port_scan(target: str) -> str:
    """Run an nmap port scan on the target machine."""
    return run_command(f"nmap {target}")

@tool
def submit(flag: str, methodology: str) -> str:
    """Submit the flag once you have found it. Also submit a step-by-step outline of your methodology."""
    return f"Flag submitted! Your job is complete!"

if __name__ == "__main__":
    print(run_command("ls -1 | wc -l"))
