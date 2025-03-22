from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from uuid import uuid4
import json

from hacker.hacker_tools import run_command, submit
from hacker.hacker_prompts import SYSTEM_PROMPT, get_user_prompt

from dotenv import load_dotenv
load_dotenv()

class HackerAgent:
    def __init__(self):
        llm = init_chat_model("o3-mini", model_provider="openai")
        tools = [
            run_command,
            submit,
        ]
        memory = MemorySaver()

        self.agent = create_react_agent(llm, tools, checkpointer=memory, prompt=SYSTEM_PROMPT)

    def run(self, target: str) -> str | None:
        config = {
            "configurable": {
                "thread_id": str(uuid4()),
                "recursion_limit": 50,
            },
        }
        user_prompt = get_user_prompt(target)

        stream = self.agent.stream(
            {"messages": [HumanMessage(content=user_prompt)]},
            config=config,
            stream_mode="values",
        )

        flag = None
        for step in stream:
            message = step["messages"][-1]
            message.pretty_print()

            if hasattr(message, "tool_calls"):
                for tool_call in message.tool_calls:
                    if tool_call["name"] == "submit":
                        try:
                            flag_arg = json.loads(tool_call["function"]["arguments"])
                            flag = flag_arg.get("flag", None)
                        except Exception as e:
                            print(f"Error extracting flag: {e}")
                        break
        return flag

if __name__ == "__main__":
    hacker = HackerAgent()
    hacker.run("London")
