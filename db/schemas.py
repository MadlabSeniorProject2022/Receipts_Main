from typing import List
from datetime import datetime
from pydantic import BaseModel
from pydantic.schema import Optional

class Item(BaseModel): 
    # id: int
    nameItem: Optional[str]
    qty: Optional[float]
    unitQty: Optional[str]
    pricePerQty: Optional[float]
    priceItemTotal: Optional[float]
    class Config:
        orm_mode = True

class EditItem(BaseModel): 
    id: Optional[int]
    nameItem: Optional[str]
    qty: Optional[float]
    unitQty: Optional[str]
    pricePerQty: Optional[float]
    priceItemTotal: Optional[float]
    class Config:
        orm_mode = True

class ResponseEditReceipt(BaseModel): 
    # about receipt
    # id: int
    receiptID: Optional[str]
    dateReceipt: Optional[datetime]
    # about shop
    shopName: Optional[str]
    taxIDShop: Optional[str]
    addressShop: Optional[str]
    shopPhone: Optional[str]
    # about customer
    customerName: Optional[str]
    taxIDCust: Optional[str]
    addressCust: Optional[str]
    class Config:
        orm_mode = True

class RequestEditReceipt(BaseModel): 
    # about receipt
    # id: int
    receiptID: Optional[str]
    dateReceipt: Optional[str]
    # about shop
    shopName: Optional[str]
    taxIDShop: Optional[str]
    addressShop: Optional[str]
    shopPhone: Optional[str]
    # about customer
    customerName: Optional[str]
    taxIDCust: Optional[str]
    addressCust: Optional[str]
    type_item: Optional[int]
    type_receipt: Optional[int]
    class Config:
        orm_mode = True

class SubmitEditItem(BaseModel):
    editItem: List[EditItem]
    deleteItem: List[int]
    dataReceipt: RequestEditReceipt
    class Config:
        orm_mode = True    

class EditReceipt(BaseModel): 
    # about receipt
    # id: int
    receiptID: Optional[str]
    dateReceipt: Optional[datetime]
    # about shop
    shopName: Optional[str]
    taxIDShop: Optional[str]
    addressShop: Optional[str]
    shopPhone: Optional[str]
    # about customer
    customerName: Optional[str]
    taxIDCust: Optional[str]
    addressCust: Optional[str]
    class Config:
        orm_mode = True

class ReceiptCreateMain(BaseModel):
    # about receipt
    filename: Optional[str]
    pathImage: Optional[str]
    receiptID: Optional[str]
    dateReceipt: Optional[datetime]
    # about shop
    shopName: Optional[str]
    taxIDShop: Optional[str]
    addressShop: Optional[str]
    shopPhone: Optional[str]
    # about customer
    customerName: Optional[str]
    taxIDCust: Optional[str]
    addressCust: Optional[str]
    status: Optional[int]
    type_item: Optional[int]
    type_receipt: Optional[int]
    # about item
    items: List[Item]
    # priceTotal: float
    class Config:
        orm_mode = True

class ResponseShop(BaseModel):
    id: int
    shopName: str
    taxIDShop: str
    addressShop: str
    shopPhone: str

class ResponseCustomer(BaseModel):
    id: int
    customerName: str
    taxIDCust: str
    addressCust: str

class ResponseItem(BaseModel):
    id: int
    nameItem: str
    qty: Optional[float]
    unitQty: Optional[str]
    pricePerQty: Optional[float]
    priceItemTotal: float
    owner_receiptId: int
    class Config:
        orm_mode = True

class ResponseGetOneReceipt(BaseModel):
    id: int
    # about receipt
    pathImage: str
    receiptID: str
    dateReceipt: Optional[datetime]
    shopID: int
    shopName: str
    taxIDShop: Optional[str]
    shopPhone: Optional[str]
    addressShop: Optional[str]
    customerID: Optional[str]
    customerName: Optional[str]
    taxIDCust: Optional[str]
    addressCust: Optional[str]
    status: Optional[int]
    type_item: Optional[int]
    type_receipt: Optional[int]
    # purchase_id: int
    # priceTotal: float
    items: List[Item] 
    class Config:
        orm_mode = True

class ResponseReceiptAll(BaseModel):
    id: int
    filename: Optional[str]
    pathImage: Optional[str]
    receiptID: Optional[str]
    dateReceipt: Optional[datetime]
    shopName: Optional[str]
    customerName: Optional[str]
    Created_At: datetime
    class Config:
        orm_mode = True

class ResponseStatusReceiptAll(BaseModel):
    id: int
    filename: str
    status: int
    Created_At: Optional[datetime]
    Updated_At: Optional[datetime]
    class Config:
        orm_mode = True

class ResponseCreateReceipt(BaseModel):
    status: str
    class Config:
        orm_mode = True

class ResponseDeleteReceipt(ResponseCreateReceipt):
    pass

class ResponseAnalyzeReceipt(BaseModel):
    filename: Optional[str]
    pathImage: Optional[str]
    receiptID: Optional[str]
    dateReceipt: Optional[datetime]
    shopName: Optional[str]
    shopPhone: Optional[str]
    taxIDShop: Optional[str]
    taxIDCust: Optional[str]
    addressShop: Optional[str]
    customer: Optional[str]
    addressCust: Optional[str]
    type_item: Optional[int]
    type_receipt: Optional[int]
    status: Optional[int]
    items: List[Item] = []
    class Config:
        orm_mode = True

class ResponseShopAll(BaseModel):
    id: int
    shopName: str
    taxIDShop: Optional[str]
    shopPhone: Optional[str]
    addressShop: Optional[str]
    class Config:
        orm_mode = True

class ResponseCustomerAll(BaseModel):
    id: int
    customerName: Optional[str]
    taxIDCust: Optional[str]
    addressCust: Optional[str]
    class Config:
        orm_mode = True

class DeleteManyItem(BaseModel):
    listDelete: List[int]
    class Config:
        orm_mode = True