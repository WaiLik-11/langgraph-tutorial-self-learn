"""
Creates a form of memory for our agents.
"""

import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages : List[Union[HumanMessage, AIMessage]]


google_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

def process(state: AgentState) -> AgentState:
    """ This node will solve the request you input """

    response = google_llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")
    print(f"CURRENT STATE: ", state["messages"])

    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

conversation_history = []

user_input = input("Enter: ")

while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))

    result = agent.invoke({ "messages": conversation_history})

    conversation_history = result["messages"]

    user_input = input("Enter: ")

with open("logging.txt", "w") as file:
    file.write("Your conversation Log History:\n")
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"Human: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n")
    file.write("\nEnd of conversation log.")

print("Conversation saved to logging.txt")

