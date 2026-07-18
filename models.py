from sqlalchemy import Column, Integer, String
from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    customer_name = Column(String)
    status = Column(String)
    item_name = Column(String)