from fastapi import APIRouter, status
from schemas import *
import services

router = APIRouter(prefix="/trips",tags=["trips"])

@router.post(
    "/",
    response_model=TripResponse,
    status_code=status.HTTP_201_CREATED
)
def create_trip(trip: TripCreate):
    return services.create_trip(trip)


@router.get(
    "/{trip_id}",
    response_model=TripResponse,
    status_code= status.HTTP_200_OK
)
def get_trip(trip_id: str):
    return services.get_trip(trip_id)

@router.put(
    "/{trip_id}",
    response_model=TripResponse,
    status_code= status.HTTP_200_OK
)
def update_trip(trip_id:str, trip:TripUpdate):
    return services.update_trip(trip_id,trip)

@router.delete(
    "/{trip_id}",
    status_code=status.HTTP_200_OK
)
def delete_trip(trip_id: str):
    return services.delete_trip(trip_id)


@router.post(
    "/{trip_id}/expenses",
    response_model=ExpenseResponse,
    status_code=status.HTTP_200_OK
)
def create_expense(trip_id: str, expense: ExpenseCreate):
    expense.trip_id=trip_id
    return services.create_expense(expense)

@router.get(
    "/{trip_id}/expenses",
    response_model=list[ExpenseResponse],
    status_code=status.HTTP_200_OK
)
def get_trip_expenses(trip_id: str):
    return services.get_trip_expenses(trip_id)

@router.get(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse,
    status_code=status.HTTP_200_OK
)
def get_expense(expense_id: str):
    return services.get_expense(expense_id)

@router.put(
    "/expense/{expense_id}",
    response_model=ExpenseResponse,
    status_code=status.HTTP_200_OK
)
def update_expense(expense_id: str, expense: ExpenseUpdate):
    return services.update_expense(expense_id, expense)

@router.delete(
    "/expenses/{expense_id}",
    status_code=status.HTTP_200_OK
)
def dalete_expense(expense_id: str):
    return services.delete_expense(expense_id)

@router.get(
    "/{trip_id}/summary",
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK
)
def get_trip_summary(trip_id:str):
    return services.get_trip_summary(trip_id)