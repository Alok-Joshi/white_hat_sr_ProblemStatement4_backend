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

def create_user(email="xy@gmail.com", password="password"):
    #check if email already exists, if yes return NONE else return true
    user = db.user
    res = list(user.find({"email":email}))
    if len(res)==0:
        #no user with this email exists
        userdata = {"email": email, "password":password}
        user.insert_one(userdata)
        return True
    else:
        #user exists
        return None

def create_contiguous_booking(email, count, time):
    #TODO: write booking algorithm
    #if can book seats mutex lock, and return table(s) allocated else return NONE
    table = db.table
    res = table.find({"$and":[{"bookings.from":time}, {"bookings.to":time+datetime.timedelta(minutes=30)}]})
    if len(list(res))==0:
        #no bookings for given timeslot for any table
        #first =
        pass
    return None

def create_order(email, items, time):
    #place order, and return orderID
    #TODO: algorithm to create uinque order id(seq numbers)
    return None

def get_menu(canteen_id=1):
    #return menu items list with price
    menu = db.menu
    res = menu.find_one({"canteen_id":canteen_id})
    if res==None:
        return None
    return res.get('items')


print(get_menu())
