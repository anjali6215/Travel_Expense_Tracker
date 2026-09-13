import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI=os.getenv("MONGO_URI","mongodb://localhost:27017")
    MONGO_DATABASE=os.getenv("MONGO_DATABASE","travel_expense_db")
    TRIP_COLLECTION=os.getenv("TRIP_COLLECTION","trips")
    EXSPENSE_COLLECTION=os.getenv("COLLECTION_NAME","expenses")
    
settings=Settings()

# if __name__=="__main__":
#     print("MONGO_URI",settings.MONGO_URI)
#     print("MONGO_DATABASE",settings.MONGO_DATABASE)
#     print("TRIP_COLLECTION",settings.TRIP_COLLECTION)
#     print("EXPENSE_COLLECTION",settings.EXSPENSE_COLLECTION)