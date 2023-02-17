import pymongo
import datetime

SERVER_URL = 'mongodb+srv://shreyas22010793:A1Hn12yTvIvx21fw@cluster0.8dvqlye.mongodb.net/?retryWrites=true&w=majority'
client = pymongo.MongoClient(SERVER_URL)
db = client.test2DB



def get_new_order(time_quantum):
    """ Blocking call to check for new orders """
    
    cursor = db["order"]
    order_document = next(cursor)

    if('fullDocument' in order_document): #Implies that a new order has been added

            order_document =  order_document['fullDocument']
            now = datetime.datetime.now()
            if(order_document["from"] >= now and order_document["to"] <= (now+datetime.timedelta(hours=time_quantum))):
                return order_document

    else:

        return None



def get_order_update(order_id: int):
    """ Blocking call to get order updates """
    
    cursor = db["order"]
    order_document = next(cursor)

    if('updateDescription' in order_document): #Implies that a new order has been added

        if(order_document['documentKey']['_id'] == order_id):
            return order_document['updateDescription']['updatedFields']
    else:

        return None
