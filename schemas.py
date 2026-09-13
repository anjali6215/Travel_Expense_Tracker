from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class TripCreate(BaseModel):
    name: str = Field(min_length=1)
    destination: str = Field(min_length=1)
    start_date: date
    end_date: date
    members: list[str] =Field(min_length=1)
    
class TripUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    destination: Optional[str]=Field(default=None,min_length=1)
    start_date: Optional[date]= None
    end_date: Optional[date]=None
    members: Optional[list[str]]=Field(default=None, min_length=1)
    
    
class TripResponse(BaseModel):
    id:str
    name: str
    destination: str
    start_date: date
    end_date: date
    members:list[str]
    
    
class ExpenseCreate(BaseModel):
    trip_id: str
    title: str= Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    paid_by: str = Field(min_length=1)
    shared_by : list[str]= Field(min_length=1)
    date: date
    description: Optional[str]=None
    
    
class ExpenseUpdate(BaseModel):
    title: Optional[str]= Field(default=None,min_length=1)
    amount: Optional[float] = Field(default=None,gt=0)
    category: Optional[str] = Field(default=None,min_length=1)
    paid_by: Optional[str] = Field(default=None,min_length=1)
    shared_by : Optional[list[str]]= Field(default=None,min_length=1)
    date: Optional[date]=None
    description: Optional[str]=None
    
class ExpenseResponse(BaseModel):
    id: str
    trip_id: str
    title: str
    amount: float 
    category: str 
    paid_by: str 
    shared_by : list[str]
    date: date
    description: Optional[str]=None
    
class SummaryResponse(BaseModel):
    trip_id: str
    total_expenses: float
    total_paid: dict[str,float]
    total_share: dict[str, float]
    balances: dict[str,float]