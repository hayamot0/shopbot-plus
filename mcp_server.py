from mcp.server.fastmcp import FastMCP
from rag import load_rag_pipeline
from models import Order
from database import SessionLocal
from dotenv import load_dotenv

load_dotenv()

mcp= FastMCP("shopbotplus")

rag_chain=load_rag_pipeline()

@mcp.tool(name="search_knowledge_base")
def search_knowledge_base(question:str):
    """Search the knowledge base for product and policy information."""
    response=rag_chain.invoke(question)
    return response


@mcp.tool(name="check_order_status")
def check_order_status(order_id: str):  
    """Search the database to return order status"""
    db=SessionLocal()
    result=db.query(Order).filter(Order.order_id == order_id).first()
    db.close()
    if result:
        return f"Order {order_id}: item={result.item_name}, status={result.status}, customer={result.customer_name}"
    
    return f"Order not found with id: {order_id}"


@mcp.prompt(name="prompt")
def prompt():
    return "You are ShopBot+, an AI assistant for an online store. You have access to two tools:" \
    " check order status by order ID, and search the knowledge base for product and policy information."

if __name__=="__main__":
    mcp.run()

