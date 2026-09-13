from bson import ObjectId
from database import *
from schemas import *
from datetime import datetime
from fastapi import HTTPException

def trip_helper(trip: dict)-> dict:
    return{
        "id": str(trip["_id"]),
        "name": trip["name"],
        "destination": trip["destination"],
        "start_date": trip["start_date"],
        "end_date": trip["end_date"],
        "members": trip["members"]
    }
    

def create_trip(trip: TripCreate):
    collection= get_trips_collection()
    
    new_trip_dict=trip.model_dump()
    new_trip_dict["start_date"]= datetime.combine(
        new_trip_dict["start_date"],
        datetime.min.time()
        )
    new_trip_dict["end_date"]= datetime.combine(
            new_trip_dict["end_date"],
            datetime.min.time()
            )
    result= collection.insert_one(new_trip_dict)
    created_trip= collection.find_one({"_id":result.inserted_id})
    
    return trip_helper(created_trip)

def get_trip(trip_id: str):
    collection=get_trips_collection()
    
    result=collection.find_one({"_id": ObjectId(trip_id)})
    
    if result:
        return trip_helper(result)
    raise HTTPException(status_code=404, detail="Trip not found")

    
def update_trip(trip_id: str,trip_data: TripUpdate):
    collection=get_trips_collection()
    if not ObjectId.is_valid(trip_id):
        raise HTTPException(status_code=400, detail="Invalid trip ID")
    updated_data= trip_data.model_dump(exclude_none=True)
    
    if "start_date" in updated_data:
        updated_data["start_date"]= datetime.combine(
        updated_data["start_date"],
        datetime.min.time()
        )
    if "end_date" in updated_data:
        updated_data["end_date"]= datetime.combine(
                updated_data["end_date"],
                datetime.min.time()
                )
        
    if not updated_data:
        return get_trip(trip_id)
    
    result= collection.update_one(
        {"_id": ObjectId(trip_id)},
        {"$set": updated_data}
    ) 
    
    if result.modified_count>0:
        updated_trip=collection.find_one({"_id":ObjectId(trip_id)})
        return trip_helper(updated_trip)
    
    raise HTTPException(status_code=404,detail="trip not found")


def delete_trip(trip_id: str):
    collection=get_trips_collection()
    if not ObjectId.is_valid(trip_id):
            raise HTTPException(status_code=400, detail="Invalid trip ID")
    
    result=collection.delete_one({"_id": ObjectId(trip_id)})
    if result.deleted_count>0:
        return {"message": "Trip deleted successfully"}
    
    raise HTTPException(status_code=404, detail="trip not found")


def expense_helper(expense: dict)-> dict:
    return{
        "id": str(expense["_id"]),
        "trip_id": expense["trip_id"],
        "title": expense["title"],
        "amount": expense["amount"],
        "category": expense["category"],
        "paid_by": expense["paid_by"],
        "shared_by": expense["shared_by"],
        "date":expense["date"],
        "description": expense.get("description")
    }
    
def create_expense(expense: ExpenseCreate):
    collection=get_expenses_collection()
    
    new_expenses_dict=expense.model_dump()
    
    new_expenses_dict["date"] = datetime.combine(
        new_expenses_dict["date"],
        datetime.min.time()
    )
    
    result=collection.insert_one(new_expenses_dict)
    
    created_expense=collection.find_one({
        "_id":result.inserted_id
    })
    
    return expense_helper(created_expense)

def get_expense(expense_id: str):
    collection=get_expenses_collection()
    
    if not ObjectId.is_valid(expense_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid expense ID"
        )
        
    result=collection.find_one({"_id":ObjectId(expense_id)})
    if result:
        return expense_helper(result)
    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


def get_trip_expenses(trip_id: str):
    collection=get_expenses_collection()
    
    if not ObjectId.is_valid(trip_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid trip ID"
        )
        
    result=collection.find({
        "trip_id":trip_id
    })
    
    return [expense_helper(expense) for expense in result]


    
def update_expense(expense_id: str, expense_data: ExpenseUpdate):
    collection=get_expenses_collection()
    
    if not ObjectId.is_valid(expense_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid trip ID"
            )
    updated_data= expense_data.model_dump(exclude_none=True)
    
    if "date" in updated_data:
        updated_data["date"] = datetime.combine(
            updated_data["date"],
            datetime.min.time()
        )
    if not updated_data:
        return get_expense(expense_id)
    
    result = collection.update_one(
        {"_id":ObjectId(expense_id)},
        {"$set": updated_data}
    )
    
    if result.modified_count>0:
        updated_expense=collection.find_one(
            {"_id": ObjectId(expense_id)}
        )
        return expense_helper(updated_expense)
    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )
    

def delete_expense(expense_id: str):
    collection= get_expenses_collection()
    if not ObjectId.is_valid(expense_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid expense ID"
        )
    result = collection.delete_one(
        {
        "_id":ObjectId(expense_id)
        }
    )
    
    if result.deleted_count > 0:
        return {"message": "Expense deleted successfully"}
    
    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )
        

def get_trip_summary(trip_id: str):
    collection= get_expenses_collection()
    if not ObjectId.is_valid(trip_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid trip ID"
        )
    expenses = collection.find({
        "trip_id":trip_id
    })
    
    Total_expenses=0
    total_paid={}
    total_share={}
    
    for expense in expenses:
        amount= expense["amount"]
        paid_by=expense["paid_by"]
        shared_by=expense["shared_by"]
        
        Total_expenses+=amount
        
        total_paid[paid_by]=total_paid.get(paid_by,0)+amount
        
        share= amount/len(shared_by)
        
        for person in shared_by:
            total_share[person]=total_share.get(person,0)+share
            
    balances={}
        
    people=set(total_paid) | set(total_share)
        
    for person in people:
        paid=total_paid.get(person,0)
        share=total_share.get(person,0)
            
        balances[person]=paid-share
            
    return{
            "trip_id": trip_id,
            "total_expenses": Total_expenses,
            "total_paid": total_paid,
            "total_share": total_share,
            "balances": balances
        }
        

    
    