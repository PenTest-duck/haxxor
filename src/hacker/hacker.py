from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from uuid import uuid4

from hacker_tools import run_command
from hacker_prompts import SYSTEM_PROMPT

from dotenv import load_dotenv
load_dotenv()

class Hacker:
    def __init__(self):
        llm = init_chat_model("gpt-4o-mini", model_provider="openai")
        tools = [
            run_command,
        ]
        memory = MemorySaver()

        self.agent = create_react_agent(llm, tools, checkpointer=memory, prompt=SYSTEM_PROMPT)

    def run(self, target: str):
        config = {"configurable": {"thread_id": str(uuid4())}}
        user_prompt = f"Target IP address: {target}"

        stream = self.agent.stream(
            {"messages": [HumanMessage(content=user_prompt)]},
            config=config,
            stream_mode="values",
        )
        for step in stream:
            step["messages"][-1].pretty_print()


if __name__ == "__main__":
    hacker = Hacker()
    hacker.run("London")
