from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

@tool
def multiply(a: int, b: int) -> int:
  """두 정수를 곱합니다"""
  return a * b

llm = ChatOpenAI(model="gpt-4o-mini")
agent_llm = llm.bind_tools([multiply])

# 3. 에이전트 노드 함수
def agent(state: MessagesState):
  response = agent_llm.invoke(state["messages"])
  return {"messages": [response]}

# 4. 그래프 생성
builder = StateGraph(MessagesState)

builder.add_node("agent", agent)
builder.add_node("tools", ToolNode([multiply]))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

result = graph.invoke({
  "messages": [
    {"role": "user", "content": "37곱하기 21 계산해줘. 아무 도구를 사용하지 마."}
  ]
})

for msg in result["messages"]:
  print(msg.type, msg.content)