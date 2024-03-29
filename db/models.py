from sqlalchemy import  Column,\
                        ForeignKey,\
                        Integer,\
                        String,\
                        DateTime,\
                        TIMESTAMP,\
                        FLOAT

from sqlalchemy.orm import relationship
from .database import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True) # PK
    filename = Column(String(250), index=True)
    pathImage = Column(String(1000), index=True)
    receiptID = Column(String(250), index=True)
    dateReceipt = Column(DateTime, index=True)
    items = relationship("Item", back_populates="owner_receipt") # FK
    shopName = Column(String(250), index=True)
    taxIDShop = Column(String(100), index=True)
    shopPhone = Column(String(100), index=True)
    addressShop = Column(String(250), index=True)   
    customerName = Column(String(250), index=True)
    taxIDCust = Column(String(100), index=True)
    addressCust = Column(String(250), index=True)
    # 0 -> without qty, 1 -> with qty
    type_item = Column(Integer, index=True)
    # 0 is not complete, 1 is ocr finished, 2 is already check (availble show), 3 is ocr fail
    type_receipt = Column(Integer, index=True)
    status = Column(Integer, index=True) 
    
    Created_At = Column(TIMESTAMP)
    Updated_At = Column(TIMESTAMP)

class Item(Base): # back to Receipt
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    nameItem = Column(String(250), index=True)
    qty = Column(FLOAT, index=True)
    unitQty = Column(String(10), index=True)
    pricePerQty = Column(FLOAT, index=True)
    priceItemTotal = Column(FLOAT, index=True)

    owner_receiptId = Column(Integer, ForeignKey("receipts.id"))
    owner_receipt = relationship("Receipt", back_populates="items")

"""
class Shop(Base): # back to Receipt
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    shopName = Column(String(250), index=True)
    taxIDShop = Column(String(30), index=True)
    shopPhone = Column(String(30), index=True)
    addressShop = Column(String(250), index=True)

class Customer(Base): # back to Receipt
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customerName = Column(String(250), index=True)
    taxIDCust = Column(String(30), index=True)
    addressCust = Column(String(250), index=True)
"""

    