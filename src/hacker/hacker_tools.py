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

if __name__ == "__main__":
    print(run_command("ls -1 | wc -l"))
