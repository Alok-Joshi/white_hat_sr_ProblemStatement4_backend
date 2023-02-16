from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import jwt
import datetime


origins = [ '*' ]

app = FastAPI()
o_auth: dict[str,str] = {} #to store the jwt and its corrsponding o_auth

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
    pass


@app.post("/register", dependencies=[Depends(check_jwt_token)],status_code = 200)
def register(pl : payload):
    pass

@app.get("/booking", dependencies=[Depends(check_jwt_token)],status_code = 200)
def get_bookings():
    pass

@app.post("/booking", dependencies=[Depends(check_jwt_token)],status_code = 200)
def book_table(bk: booking,token: str = Header(None)):

    booking_result = database.create_contiguous_booking(bk.seat_count);
    if(booking_result is not None):
        #create the order
        o_auth_token = o_auth[token]
        order_creation_result = database.create_order(o_auth_token,booking.order)

        if(order_creation_result is not None):
            #TODO: Return a  dictionary denoting success
        else:
            #TODO: return a dictionary denoting failure to create order (with reason)
    else:
        #TODO: return a dictionary denoting failure to book (with reason)

    pass

#@app.get("/orders", dependencies=[Depends(check_jwt_token)],status_code = 200)
#def get_orders():

