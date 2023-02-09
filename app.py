# built in module
from typing import List
from fastapi import FastAPI, Request, File, UploadFile, status, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_pagination import Page, paginate, add_pagination
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from functools import wraps
# from werkzeug.utils import secure_filename
import cv2
import numpy as np

# my module
from mainModule import runMain # main application of project

from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Final Project", debug=True)

add_pagination(app)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


#################################### Default Module #################################### 

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/listreceipts/", response_class=HTMLResponse)
def getlistReceiptAllPage(request: Request, db: Session = Depends(get_db)):
    list_data = crud.getReceiptByAll(db)
    return templates.TemplateResponse("listReceipt.html", {"request": request, "list_data": list_data})

@app.get("/listshops/", response_class=HTMLResponse)
def getlistShopByPagination(request: Request, db: Session = Depends(get_db)):
    list_data = crud.getShopAll(db)
    return templates.TemplateResponse("listShop.html", {"request": request, "list_data": list_data})

@app.get("/listcustomers/", response_class=HTMLResponse)
def getlistCustomerByPagination(request: Request, db: Session = Depends(get_db)):
    list_data = crud.getCustomerAll(db)
    return templates.TemplateResponse("listCustomer.html", {"request": request, "list_data": list_data})

#################################### Receipt Module #################################### 

@app.post("/receipts/create/", tags = ["Receipts"], response_model=schemas.ResponseCreateReceipt)
async def createReceipt(receipt: schemas.ReceiptCreateMain, db: Session = Depends(get_db)):
    return await crud.create_receipt_main(db=db, receipt=receipt)

@app.post("/receipts/analyze/", tags = ["Receipts"], response_model=schemas.ResponseAnalyzeReceipt)
async def analyzeReceipt(file: UploadFile, request: Request):
    image = cv2.imdecode(np.fromstring(file.file.read(), np.uint8),\
            cv2.IMREAD_UNCHANGED)
    # path_file = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)           
    data = runMain(image)
    path_file = "img/" + file.filename
    data["pathImage"] = "/static/"+path_file
    data["filename"] = file.filename
    # print(data)
    # await file.seek(0)
    with open("static/"+path_file, "wb+") as file_object:
        file_object.write(file.file.read())
    # redirect_url = request.url_for('home')   
    # return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    return data

@app.get("/receipts/getOneByID/{receipt_id}", tags = ["Receipts"], response_model=schemas.ResponseGetOneReceipt)
def getOneReceipt(receipt_id: int, db: Session = Depends(get_db)):
    db_receipt = crud.getOneReceiptByID(db, id = receipt_id)
    if db_receipt is None:
        raise HTTPException(status_code=404, detail="Receipt not found with the given ID")
    return crud.getOneReceipt_byDBId_main(db, receipt_id)

@app.get("/receipts/getByPagination/", tags = ["Receipts"], response_model=Page[schemas.ResponseReceiptAll])
def getReceiptByPagination(db: Session = Depends(get_db)):
    return paginate(crud.getReceiptByAll(db))

@app.delete('/receipts/deleteReceiptByID/{receipt_id}', tags = ["Receipts"], response_model=schemas.ResponseDeleteReceipt)
async def removeOneReceipt_byIndex(receipt_id: int, db: Session = Depends(get_db)):
    db_receipt = crud.getOneReceiptByID(db, id = receipt_id)
    if db_receipt is None:
        raise HTTPException(status_code=404, detail="Receipt not found with the given ID")
    crud.removeOneReceipt_byIndex(db, id = receipt_id)
    return {"status": "success"}

#################################### Shop Module #################################### 

@app.get("/shops/getShopAll", tags = ["shops"], response_model=Page[schemas.ResponseShopAll])
def getShopAll(db: Session = Depends(get_db)):
    return paginate(crud.getShopAll(db))

#################################### Customer Module #################################### 

@app.get("/customers/getCustomerAll", tags = ["customers"], response_model=Page[schemas.ResponseCustomerAll])
def getCustomerAll(db: Session = Depends(get_db)):
    return paginate(crud.getCustomerAll(db))
