from typing import Annotated
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt
from uuid import uuid4
from dotenv import load_dotenv
load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

class Hacker():
    def __init__(self):
        self.config = {
            "configurable": {
                "thread_id": str(uuid4())
            }
        }

        memory = MemorySaver()
        tools = [
            self.get_weather,
            # self.human_assistance,
        ]
        tool_node = ToolNode(tools=tools)

        raw_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        self.llm = raw_llm.bind_tools(tools)

        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", self.chatbot)
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")
        graph_builder.set_entry_point("chatbot")
        self.graph = graph_builder.compile(checkpointer=memory)

    def chatbot(self, state: State):
        return {"messages": [self.llm.invoke(state["messages"])]}

    @tool
    def get_weather(city: str) -> str:
        """Retrieve the weather for a given city."""
        return f"The weather in {city} has a temperature of 26.7°C and is partly cloudy."

    @tool
    def human_assistance(query: str) -> str:
        """Request assistance from a human."""
        human_response = interrupt({"query": query})
        return human_response["data"]

    def stream_graph_updates(self, user_prompt: str):
        events = self.graph.stream(
            {"messages": [{"role": "user", "content": user_prompt}]},
            config=self.config,
            stream_mode="values",
        )
        for event in events:
            event["messages"][-1].pretty_print()

    def run(self, target: str):
        while True:
            user_prompt = input("User: ")
            if user_prompt.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            self.stream_graph_updates(user_prompt)

if __name__ == "__main__":
    hacker = Hacker()
    hacker.run("1.1.1.1")