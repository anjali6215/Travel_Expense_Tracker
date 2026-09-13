from pymongo import MongoClient
from config import settings

_client: MongoClient| None = None 

def connect() -> None:
    global _client
    
    _client=MongoClient(settings.MONGO_URI,serverSelectionTimeoutms=5000)
    
    # __client.admin.command("ping")
    print("MongoDB connection successfull!")
    
    
def get_client() -> MongoClient:
    if _client is None:
        connect()
    return _client

def get_database():
    return get_client()[settings.MONGO_DATABASE]

def get_trips_collection():
    return get_database()[settings.TRIP_COLLECTION]

def get_expenses_collection():
    return get_database()[settings.EXSPENSE_COLLECTION]

def disconnect()->None:
    global _client
    
    if _client is not None:
        _client.close()
        _client=None
        
        print("MongoDB disconnected!")


# if __name__=="__main__":
#     connect()
#     print(get_database().name)
#     print(get_trips_collection().name)
#     print(get_expenses_collection().name)

#     disconnect()
    
