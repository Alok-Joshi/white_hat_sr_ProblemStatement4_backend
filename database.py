import pymongo
client = pymongo.MongoClient('mongodb+srv://shreyas22010793:A1Hn12yTvIvx21fw@cluster0.8dvqlye.mongodb.net/?retryWrites=true&w=majority')
db = client.test2DB


def authenticate(email="xyz@gmail.com", password="password"):
    #check if user exists, and sign them in
    #return true if successful else return NONE
    user = db.user
    res = user.find_one({"email":email})
    #print(res)
    if res is not None:
        pswd = res['password']
        if pswd==password:
            return True
        else:
            return None
    return res

def create_user(email, password):
    #check if email already exists, if yes return NONE else return true
    user = db.user
    pass
def create_contiguous_booking(email, count, time):
    #TODO: write booking algorithm
    #if can book seats mutex lock, and return table(s) allocated else return NONE
    return None

def create_order(email, items, time):
    #place order, and return orderID
    #TODO: algorithm to create uinque order id(seq numbers)
    return None

def get_menu(canteen_id=1):
    #return menu items list with price
    return None


print(authenticate())
