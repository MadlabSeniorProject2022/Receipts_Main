from sqlalchemy.orm import Session
from typing import List, Union

from . import models, schemas

#################################### for get method #################################### 

async def create_receipt_main(db: Session, receipt: Union[schemas.ReceiptCreateMain, dict], type_receipt: int):
    # create shop
    # print(receipt)
    db_shop = await create_shop(
                db, 
                shopName = receipt["shopName"], 
                taxIDShop = receipt["taxIDShop"], 
                addressShop = receipt["addressShop"],
                shopPhone = receipt["shopPhone"])
    # create customer
    db_cust = await create_customer(db,
                customerName = receipt["customerName"],
                addressCust = receipt["addressCust"],
                taxIDCust = receipt["taxIDCust"])

    db_receipt = models.Receipt(
        filename = receipt["filename"],
        pathImage = receipt["pathImage"],
        receiptID = receipt["receiptID"], 
        dateReceipt = receipt["dateReceipt"],
        type_receipt = type_receipt,
        shopID = db_shop.id,
        customerID = db_cust.id
    )
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)

    await create_item(db, listItems = receipt["items"], owner_receiptId = db_receipt.id, type_receipt = type_receipt)

    return {"status": "success"}

async def create_shop(db: Session, 
                shopName: str, 
                taxIDShop: str, 
                addressShop: str,
                shopPhone: str):
    db_shop = await getOneShopName_byValue(db, 
                                     shopName = shopName,
                                     taxIDShop = taxIDShop,
                                     addressShop = addressShop,
                                     shopPhone = shopPhone)
    if db_shop is None:
        db_shop = models.Shop(
            shopName = shopName, 
            taxIDShop = taxIDShop,
            addressShop = addressShop,
            shopPhone = shopPhone
        )
        db.add(db_shop)
        db.commit()
        db.refresh(db_shop)
    return db_shop

async def create_customer(db: Session, 
                    customerName: str, 
                    addressCust: str,
                    taxIDCust: str):
    db_cust = await getOneCustomerName_byValue(db, 
                                         customerName = customerName, 
                                         addressCust = addressCust, 
                                         taxIDCust = taxIDCust)
    if db_cust is None:
        db_cust = models.Customer(
            customerName = customerName, 
            taxIDCust = taxIDCust,
            addressCust = addressCust)
        db.add(db_cust)
        db.commit()
        db.refresh(db_cust)

    return db_cust

async def create_item(db: Session, listItems: any, owner_receiptId: int, type_receipt: int):
    objects = []
    for ele in listItems:
        if type_receipt == 0:
            db_items = models.Item(
                nameItem = ele["nameItem"], 
                priceItemTotal = ele["priceItemTotal"],
                owner_receiptId = owner_receiptId
            )
        elif type_receipt == 1:
            db_items = models.Item(
                nameItem = ele["nameItem"], 
                qty = ele["qty"],
                unitQty = ele["unitQty"],
                pricePerQty = ele["pricePerQty"],
                priceItemTotal = ele["priceItemTotal"],
                owner_receiptId = owner_receiptId
            )        
        objects.append(db_items)
    db.bulk_save_objects(objects)
    db.commit()

#################################### for get method #################################### 

async def getOneShopName_byValue(db: Session, 
                           shopName: str, 
                           taxIDShop: str, 
                           addressShop: str,
                           shopPhone: str):
    return db.query(models.Shop)\
             .filter(models.Shop.shopName == shopName,
                     models.Shop.taxIDShop == taxIDShop ,
                     models.Shop.addressShop == addressShop,
                     models.Shop.shopPhone == shopPhone)\
             .first()

async def getOneCustomerName_byValue(db: Session,
                               customerName: str, 
                               addressCust: str, 
                               taxIDCust: str):
    return db.query(models.Customer)\
             .filter(models.Customer.customerName == customerName,
                     models.Customer.addressCust == addressCust,
                     models.Customer.taxIDCust == taxIDCust)\
             .first()

async def getOneReceipt_byDBId_main(db: Session, id: int):
   db_receipt = db.query(models.Receipt).filter(models.Receipt.id == id).first()
   db_shop = await getOneShop_byDBId(db, id = db_receipt.shopID)
   db_customer = await getOneCustomer_byDBId(db, id = db_receipt.customerID)
   # db_item = await getItem_byDBId(db, owner_receiptId = id)
   # print(db_item)
   return {
        'id': id,
        'filename': db_receipt.filename,
        'pathImage': db_receipt.pathImage,
        'receiptID': db_receipt.receiptID,
        'dateReceipt': db_receipt.dateReceipt,
        'type_receipt': db_receipt.type_receipt,
        'shopID': db_shop.id,
        'shopName': db_shop.shopName,
        'taxIDShop': db_shop.taxIDShop,
        'shopPhone': db_shop.shopPhone,
        'addressShop': db_shop.addressShop,
        'customerID': db_customer.id,
        'customerName': db_customer.customerName,
        'taxIDCust': db_customer.taxIDCust,
        'addressCust': db_customer.addressCust,
        # 'priceTotal': db_purchase.priceTotal,
        # 'items': db_item
   }

async def getReceiptByAll(db: Session):
    db_receipt = db.query(models.Receipt.id,
                          models.Receipt.filename,
                          models.Receipt.pathImage,
                          models.Receipt.receiptID,
                          models.Receipt.dateReceipt,
                          models.Shop.shopName,
                          models.Customer.customerName)\
                   .join(models.Customer, models.Receipt.customerID==models.Customer.id)\
                   .join(models.Shop, models.Receipt.shopID==models.Shop.id)\
                   .all()
    return db_receipt

async def getOneShop_byDBId(db: Session, id: int):
   db_shop = db.query(models.Shop).filter(models.Shop.id == id).first()
   return db_shop

async def getOneCustomer_byDBId(db: Session, id: int):
   db_customer = db.query(models.Customer).filter(models.Customer.id == id).first()
   return db_customer

async def getItem_byDBId(db: Session, owner_receiptId: int):
   db_item = db.query(models.Item).filter_by(owner_receiptId = owner_receiptId).all()
   return db_item

async def getOneItem_byDBId(db: Session, owner_receiptId: int, item_id: int):
   db_item = db.query(models.Item).filter_by(
        owner_receiptId = owner_receiptId,
        id = item_id).first()
   return db_item

async def editOneItem_byDBId(db: Session, owner_receiptId: int, item_id: int):
   db_item = db.query(models.Item).filter_by(
        owner_receiptId = owner_receiptId,
        id = item_id).first()
   return db_item

async def getShopAll(db: Session):
    db_shop = db.query(models.Shop).all()
    return db_shop

async def getCustomerAll(db: Session):
    db_cust = db.query(models.Customer).all()
    return db_cust

async def getOneReceiptByID(db: Session, id: int):
    return db.query(models.Receipt).filter(models.Receipt.id == id).first()

#################################### for delete method ####################################
async def removeOneReceipt_byIndex(db: Session, id: int):
    db_receipt = db.query(models.Receipt).filter_by(id=id).first()
    db.delete(db_receipt)
    db.commit()

#################################### for patch method ####################################
# def editOneReceipt_byIndex():
#    return None
