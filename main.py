from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from models import Order
from schemas import OrderCreate, OrderResponse, ChatRequest, ChatResponse
from langchain_core.messages import HumanMessage
from agent import app as agent_app


app=FastAPI()
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="frontend/templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")



def get_db():
    db=SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.post("/chat", response_model=ChatResponse)
def response(message: ChatRequest):
    result = agent_app.invoke({"messages": [HumanMessage(content=message.message)]})

    content = result["messages"][-1].content

    if isinstance(content, list):
        content = content[0]["text"]

    return {"response": content}


@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order =Order(order_id=order.order_id, customer_name=order.customer_name, status=order.status, item_name=order.item_name)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order_get=db.query(Order).filter(Order.order_id == order_id).first()
    if order_get is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_get

