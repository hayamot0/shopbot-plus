from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from rag import load_rag_pipeline
from database import SessionLocal
from models import Order

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def search_knowledge_base(query: str):
    """"Calls the rag pipeline and searches the knowledge base for relevant information based on the user's query """
    rag_pipeline=load_rag_pipeline()
    response=rag_pipeline.invoke(query)
    return response


@tool
def check_order_status(order_id: str):
    """Checks the status of an order based on the provided order ID."""
    db=SessionLocal()
    result=db.query(Order).filter(Order.order_id == order_id).first()
    db.close()
    if result:
        return f"Order {order_id}: item={result.item_name}, status={result.status}, customer={result.customer_name}"
    
    return f"Order not found with id: {order_id}"

tools=[search_knowledge_base, check_order_status]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0).bind_tools(tools)



def model_call(state: AgentState)->AgentState:
    system_prompt = SystemMessage(content="""You are ShopBot+, an AI customer support assistant for our online store.
You have two tools available: search_knowledge_base and check_order_status.
Answer questions ONLY using information from these tools. If a question is unrelated to our store, products, orders, or policies,
politely explain that you can only help with store-related questions — do not answer from general knowledge, even if you know the answer, 
and do not claim you can answer general questions.
Stay friendly, concise, and on-topic.""")
    response=llm.invoke([system_prompt]+state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState):
    last_message=state["messages"][-1]
    if not last_message.tool_calls:
        return END
    return "continue"
    

graph=StateGraph(AgentState)

tool_node=ToolNode(tools=tools)

graph.set_entry_point("model_call")

graph.add_node("model_call", model_call)

graph.add_conditional_edges("model_call",should_continue,{"continue":"tool_node", END: END})

graph.add_node("tool_node", tool_node)

graph.add_edge("tool_node","model_call")

app=graph.compile()


if __name__ == "__main__":
    from langchain_core.messages import HumanMessage
    result = app.invoke({"messages": [HumanMessage(content="What is your return policy?")]})
    print(result["messages"][-1].content)