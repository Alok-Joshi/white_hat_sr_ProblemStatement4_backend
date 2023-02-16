from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import jwt
import datetime
import database

origins = [ '*' ]

app = FastAPI(title = "CanteenBooking")
o_auth_token: dict[str,str] = {} #to store the jwt and its corrsponding o_auth

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = ""
EXPIRY_TIME = 60 * 24 * 7


class payload(BaseModel):
    email: str
    password: str

class order(BaseModel):
    item_id: int

class booking(BaseModel):
    seat_count: int
    order: list[order]



def get_jwt_token(email: str):
    return jwt.encode({ "email" : email ,
       'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes= EXPIRY_TIME)
    }, SECRET_KEY, )

def check_jwt_token(token : str = Header(None)):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=404, detail="JWT_TOKEN_NOT_FOUND")



@app.post("/login",status_code = 200)
def login(pl: payload):
    if pl.password == None:
        raise HTTPException(status_code=404, detail="No Password Provided")
    else:
        o_auth = database.get_o_auth(pl.email,pl.password)
        if o_auth is not None: 
                new_jwt_token = get_jwt_token(pl.email)
                o_auth_token[new_jwt_token] = o_auth
                return {"message" : "Logged In Succesfully", "token" : new_jwt_token}
        else:
                raise HTTPException(status_code=404, detail="User Not Found")


@app.post("/register", status_code = 200)
def register(pl : payload):
    if pl.password != None:

        new_user_o_auth = database.create_user(pl.email,pl.password)

        if(new_user_o_auth is not None):
                new_jwt_token = get_jwt_token(pl.email)

                o_auth_token[new_jwt_token] = new_user_o_auth
                return { "message" : "User was registered Succesfully","token" : get_jwt_token(pl.email) }

                
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

    booking_result = database.create_contiguous_booking(bk.seat_count);
    if(booking_result is not None):
        #create the order
        o_auth_tok = o_auth_token[token]
        order_creation_result = database.create_order(o_auth_tok,booking.order)

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

@app.get("/menu",dependencies= [Depends(check_jwt_token)],status_code = 200)
def get_menu():

    menu = database.get_menu();
    return menu




