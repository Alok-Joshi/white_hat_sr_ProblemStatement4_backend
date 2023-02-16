from fastapi import FastAPI, Header, HTTPException, Depends, WebSocket
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import jwt
import datetime
import database

origins = [ '*' ]

app = FastAPI(title = "CanteenBooking")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USER_SECRET_KEY = "usercanteenbooking"
ADMIN_SECRET_KEY = "adminusercanteenbooking"
EXPIRY_TIME = 60 * 24 * 7


class payload(BaseModel):
    email: str
    password: str

class order(BaseModel):
    item_id: int

class booking(BaseModel):
    seat_count: int
    orders: list[order]


class menu_item(BaseModel):
    item_name: str
    item_price : int


def get_jwt_token(email: str):
    return jwt.encode({ "email" : email ,
       'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes= EXPIRY_TIME)
    }, USER_SECRET_KEY, )

def check_jwt_token(token : str = Header(None)):
    try:
        return jwt.decode(token, USER_SECRET_KEY, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=404, detail="JWT_TOKEN_NOT_FOUND")

def get_jwt_admin_token(email: str):
    return jwt.encode({ "email" : email ,
       'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes= EXPIRY_TIME)
    }, ADMIN_SECRET_KEY, )

def check_jwt_admin_token(token : str = Header(None)):
    try:
        return jwt.decode(token, ADMIN_SECRET_KEY, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=404, detail="JWT_TOKEN_NOT_FOUND")




@app.post("/login",status_code = 200)
def login(pl: payload):
    if pl.password == None:
        raise HTTPException(status_code=404, detail="No Password Provided")
    else:
        auth_success = database.authenticate(pl.email,pl.password)
        if auth_success is not None: 
                new_jwt_token = get_jwt_token(pl.email)
                return {"message" : "Logged In Succesfully", "token" : new_jwt_token}
        else:
                raise HTTPException(status_code=404, detail="User Not Found")


@app.post("/register", status_code = 200)
def register(pl : payload):
    if pl.password != None:

        new_user_result = database.create_user(pl.email,pl.password)
        if(new_user_result is not None):
                new_jwt_token = get_jwt_token(pl.email)
                return { "message" : "User was registered Succesfully","token" : new_jwt_token}
                
        else:
                raise HTTPException(status_code=404, detail="User Already exists")

    else:
        raise HTTPException(status_code = 404, detail = "No password entered")



@app.get("/booking", dependencies=[Depends(check_jwt_token)],status_code = 200)
def get_bookings():
    #implement in future when there is a need to display bookings like bookmyshow
    pass

@app.post("/booking", dependencies=[Depends(check_jwt_token)],status_code = 200)
def book_table(bk: booking,token: str = Header(None)):

    email = jwt.decode(token,options = {"verify_signature":False})["email"]
    booking_result = database.create_contiguous_booking(email,bk.seat_count);
    if(booking_result is not None):
        #create the order
        order_creation_result = database.create_order(email,booking.orders)

        if(order_creation_result is not None):
            #TODO: Return a  dictionary denoting success
            pass
        else:
            #TODO: return a dictionary denoting failure to create order (with reason)
            pass
    else:
        #TODO: return a dictionary denoting failure to book (with reason)
        pass




#MENU Endpoints

@app.get("/menu/{canteen_id}",dependencies= [Depends(check_jwt_token)],status_code = 200)
def get_menu(canteen_id:int):

    menu = database.get_menu(canteen_id)
    return menu


@app.post("/menu/{canteen_id}",dependencies= [Depends(check_jwt_admin_token)],status_code = 200)
def add_item(mu: menu_item,canteen_id:int):
    pass

@app.put("/menu/{canteen_id}",dependencies= [Depends(check_jwt_admin_token)],status_code = 200)
def update_item(mu: menu_item,canteen_id:int):
    pass

#@app.("/menu/{canteen_id}",dependencies= [Depends(check_jwt_admin_token)],status_code = 200)
#def update_item(mu: menu_item,canteen_id:int):
#    pass


#LISTENERS 
@app.websocket("/ws/notifications/orderstatus/{order_id}")
async def order_status(websocket: WebSocket, order_id: str):

    await websocket.accept()
    while True:
        client_data = await websocket.receive_text()
        modified_order_document = database.check_order_document(order_id)
        modified_order_document_string = json.dumps(modified_order_document)
        await websocket.send_text(modified_order_document)


@app.websocket("/ws/notifications/neworders/{canteen_id}")
async def new_order(websocket: WebSocket):

    await websocket.accept()
    while True:
        client_data = await websocket.receive_text()
        new_ord = database.check_new_order()
        new_ord_string = json.dumps(new_ord)
        await websocket.send_text(new_ord_string)
        


#ADMIN ENDPOINTS

@app.post("/admin/login",status_code = 200)
def admin_login(pl: payload):
    if pl.password == None:
        raise HTTPException(status_code=404, detail="No Password Provided")
    else:
        auth_success = database.authenticate_admin(pl.email,pl.password)
        if auth_success is not None: 
                new_jwt_token = get_jwt_admin_token(pl.email)
                return {"message" : "Logged In Succesfully", "token" : new_jwt_token}
        else:
                raise HTTPException(status_code=404, detail="User Not Found")


@app.post("/admin/register", status_code = 200)
def admin_register(pl : payload):
    if pl.password != None:

        new_user_result = database.create_admin(pl.email,pl.password)
        if(new_user_result is not None):
                new_jwt_token = get_jwt_admin_token(pl.email)
                return { "message" : "User was registered Succesfully","token" : new_jwt_token}
                
        else:
                raise HTTPException(status_code=404, detail="User Already exists")

    else:
        raise HTTPException(status_code = 404, detail = "No password entered")




