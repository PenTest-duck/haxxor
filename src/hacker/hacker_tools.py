from textwrap import dedent
from langchain_core.tools import tool
from langgraph.types import interrupt
import subprocess

from constants import MAX_COMMAND_OUTPUT_SIZE, MAX_COMMAND_TIMEOUT

def truncate_output(output: str) -> str:
    if len(output) <= MAX_COMMAND_OUTPUT_SIZE:
        return output
    return output[:MAX_COMMAND_OUTPUT_SIZE] + "\n[Output truncated...]"

# TODO: maybe I can cache tool output for the same command?
@tool
def run_command(command: str) -> str:
    """Run a shell command. The command MUST be self-contained and non-interactive!"""
    try:
        result = subprocess.run(command, capture_output=True, shell=True, text=True, check=True, timeout=MAX_COMMAND_TIMEOUT)
        return f"<stdout>\n{truncate_output(result.stdout)}\n</stdout>"
    except subprocess.TimeoutExpired:
        return dedent(f"""
            Command timed out after {MAX_COMMAND_TIMEOUT} seconds.
            This is either because the command took too long to execute, or you have accidentally used a command that expects interactive user input.
            Try a different command or break it down into smaller steps.
        """)
    except subprocess.CalledProcessError as e:
        return f"""<exit_code>{e.returncode}</exit_code>
<stderr>
{truncate_output(e.stderr)}
</stderr>
<stdout>
{truncate_output(e.stdout)}
</stdout>"""

@tool
def ask_human_assistance(query: str) -> str:
    """Ask a human for assistance with a given query."""
    response = input(f"Query: {query}\nHuman: ")
    return response

# Rustscan faster tho?
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
