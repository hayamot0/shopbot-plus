from pydantic import BaseModel


class OrderCreate(BaseModel):
    order_id: int
    customer_name: str
    status: str
    item_name: str


class OrderResponse(BaseModel):
    id: int
    order_id: str
    customer_name: str
    status: str
    item_name: str

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str