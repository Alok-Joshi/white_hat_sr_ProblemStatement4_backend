import pymongo, datetime
client = pymongo.MongoClient('mongodb+srv://shreyas22010793:A1Hn12yTvIvx21fw@cluster0.8dvqlye.mongodb.net/?retryWrites=true&w=majority')
db = client.test2DB
order_no = 1

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

def create_contiguous_booking(email="shreyas", count=1, time=datetime.datetime(2023, 2, 17, 8,0)):
    #search for tables with available seats in timeslot given
    table = db.table
    all_tables = table.find()
    for i in all_tables:
        #iterate over all tables to fix some edge cases
        cur_table_id = i.get('_id')
        cur_table_bookings = i.get('bookings')
        if cur_table_bookings==None:
            #no future bookings on this table
            table.update_one({'_id':cur_table_id}, {'$push':{'bookings':{"from":time, "to":time+datetime.timedelta(minutes=30), "seats_booked":count, "by":[email]}}})
            return i.get('id')
        else:
            timeslot_present = False
            for j in range(len(cur_table_bookings)):
                if cur_table_bookings[j].get('from')==time and cur_table_bookings[j].get('to')==time+datetime.timedelta(minutes=30):
                    #print("true")
                    timeslot_present = True
                    cur_seats_booked_for_slot = cur_table_bookings[j].get('seats_booked') 
                    left_seats = i.get('max_seats')-cur_table_bookings[j].get('seats_booked')
                    if(left_seats == 0) or (left_seats<count):
                        #timeslot found, no seats available to book
                        #skip checks of all further slots
                        break
                    if left_seats >= count:
                        #print("Left seats: ",i.get('max_seats')-cur_table_bookings[j].get('seats_booked'))
                        #left_seats = i.get('max_seats')-cur_table_bookings[j].get('seats_booked') 
                        table.update_one({'_id':cur_table_id},{'$set':{f"bookings.{j}.seats_booked":(cur_seats_booked_for_slot+count)}, '$push':{f"bookings.{j}.by": email}})
                        return {"table_name": i.get('id')}

            if not timeslot_present:
                table.update_one({'_id':cur_table_id}, {'$push':{'bookings':{"from":time, "to":time+datetime.timedelta(minutes=30), "seats_booked":count, "by":[email]}}})
                return {"table_name": i.get('id')}
    #no table matches condition
    #that is everything is full
    return None



def create_order(email, items, time, order_type=0):
    #place order, and return orderID
    #TODO: algorithm to create uinque order id(seq numbers)
    order = db.order
    global order_no
    order_id = order_no
    order_no += 1
    data = {"id":order_id, "user_id":email, "status":"placed", "items":items, "order_type":order_type, "from":time, "to":time+datetime.timedelta(minutes=30)}

    order.insert_one(data)
    return {"order_id":order_id}
    #return None

def get_menu(canteen_id=1):
    #return menu items list with price
    menu = db.menu
    res = menu.find_one({"canteen_id":canteen_id})
    if res==None:
        return None
    return res.get('items')


print(create_order("xyz@gmial.com", ["chaha","khari"], datetime.datetime(2023, 2, 17, 11,0)))
