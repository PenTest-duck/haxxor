# Haxxor - the AI hacker

Haxxor is currently designed to hack HackTheBox and TryHackMe machines in a controlled environment.

TODO:
- Connect to HTB ✅
- Basic tool calling agent ✅
- Connect to TryHackMe
- Create tools ✅
- Truncate long outputs ✅
- Better SSH/FTP/Telnet connections - keep shell open through tool?
- Store tool output as files?
- Make tool calls async
- Allow human in the loop
  - Maybe determine whether a tool action would be destructive, and escalate to human for approval if needed
  - This depends on the direction of this tool - will it be a co-working buddy or a fully autonomous agent?
- Create sub-agents (e.g. recon, researcher, reporter)
- Have multiple generations of agents such that when an agent surrenders, it leaves a note and artifacts (/tmp) for the next lifecycle of the agent 
- Maybe I make this an interactive terminal CLI tool that collaborates with the human (`hcli`)
  - It could perform initial scan against target (or take in artifacts from a folder)
  - Persistently store sessions to keep continuous memory about a target (store workspaces for the LLM)
  - User can chat to it or ask it to do things
  - Hm... would it be LLM-driven with Human-in-the-loop or Human-driven with LLM-copilot?
- Bug bounty hunter agent?
- OSINT agent?
