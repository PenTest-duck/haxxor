import os
from typing import Any, Dict, Optional, Tuple
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from uuid import uuid4
import json
from pydantic import BaseModel

from constants import DEFAULT_MODEL_PROVIDER
from hacker.hacker_tools import ask_human_assistance, run_command, submit
from hacker.hacker_prompts import SYSTEM_PROMPT, get_user_prompt

from dotenv import load_dotenv
load_dotenv()

class HackerAgentResult(BaseModel):
    success: bool
    failure_reason: Optional[str] = None
    flag: Optional[str] = None
    methodology: Optional[str] = None

class HackerAgent:
    def __init__(self, model: str):
        llm = init_chat_model(model, model_provider=DEFAULT_MODEL_PROVIDER)
        tools = [
            run_command,
            ask_human_assistance,
            submit,
        ]
        memory = MemorySaver()

        self.agent = create_react_agent(llm, tools, checkpointer=memory, prompt=SYSTEM_PROMPT)

    def run(self, target: str, name: str) -> HackerAgentResult:
        thread_id = str(uuid4())
        config = self._get_config(thread_id, target)
        user_prompt = get_user_prompt(target)

        stream = self.agent.stream(
            {"messages": [HumanMessage(content=user_prompt)]},
            config=config,
            stream_mode="values",
        )

        os.makedirs(os.path.join("logs", name), exist_ok=True)
        with open(os.path.join("logs", name, f"{thread_id}.txt"), "w+") as f:
            flag = None
            methodology = None
            for step in stream:
                message = step["messages"][-1]
                message.pretty_print()
                f.write(f"{message.pretty_repr()}\n")

                flag, methodology = self._check_submit(message)
            
            success = flag is not None
            if success:
                f.write(f"✅ FLAG FOUND: {flag}\n")
            else:
                f.write(f"❌ FAILED TO FIND FLAG\n")
        
        return HackerAgentResult(
            success=success,
            failure_reason=None,
            flag=flag,
            methodology=methodology,
        )
    
    def _get_config(self, thread_id: str, target: str) -> Dict[str, Any]:
        return {
            "configurable": {
                "thread_id": thread_id,
            },
            "recursion_limit": 50,
            "run_name": target,
        }

    def _check_submit(self, message: Any) -> Tuple[Optional[str], Optional[str]]:
        if not hasattr(message, "tool_calls"):
            return None, None
        
        flag, methodology = None, None
        for tool_call in message.tool_calls:
            if tool_call.get("name") == "submit":
                try:
                    args = json.loads(tool_call.get("args", "{}"))
                    flag = args.get("flag")
                    methodology = args.get("methodology")
                except Exception as e:
                    print(f"Error extracting flag: {e}")
                break
        return flag, methodology

if __name__ == "__main__":
    hacker = HackerAgent()
    hacker.run("London")
