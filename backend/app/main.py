from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from app.db.connection import get_connection
from app.db.schema import initialize_database
from app.services.groups import create_group, add_member, clean_name
from app.services.expenses import create_expense
from app.db.repositories import (
    list_expenses,
    list_groups,
    list_members,
)
from app.services.balances import get_group_balances
from app.services.settlements import get_group_settlements
from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="SplitLedger API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateGroupRequest(BaseModel):
    name: str

class AddMemberRequest(BaseModel):
    name: str

class CreateExpenseRequest(BaseModel):
    payer_member_id: int
    description: str
    amount: str


@app.get("/api/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post(
    "/api/groups",
    status_code=status.HTTP_201_CREATED,
)
def create_group_endpoint(payload: CreateGroupRequest):
    connection = get_connection()

    try:
        group_id = create_group(
            connection,
            payload.name,
        )

        return {
            "id": group_id,
            "name": clean_name(payload.name),
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    finally:
        connection.close()


@app.post(
    "/api/groups/{group_id}/members",
    status_code=status.HTTP_201_CREATED,
)
def add_member_endpoint(
    group_id: int,
    payload: AddMemberRequest,
):
    connection = get_connection()

    try:
        member_id = add_member(
            connection,
            group_id,
            payload.name,
        )

        return {
            "id": member_id,
            "group_id": group_id,
            "name": clean_name(payload.name),
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    finally:
        connection.close()

@app.post(
    "/api/groups/{group_id}/expenses",
    status_code=status.HTTP_201_CREATED,
)
def create_expense_endpoint(
    group_id: int,
    payload: CreateExpenseRequest,
):
    connection = get_connection()

    try:
        expense_id = create_expense(
            connection=connection,
            group_id=group_id,
            payer_member_id=payload.payer_member_id,
            description=payload.description,
            amount=payload.amount,
        )

        return {
            "id": expense_id,
            "group_id": group_id,
            "payer_member_id": payload.payer_member_id,
            "description": payload.description.strip(),
            "amount": payload.amount,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    finally:
        connection.close()


@app.get("/api/groups/{group_id}/balances")
def get_balances_endpoint(group_id: int):
    connection = get_connection()

    try:
        members = list_members(connection, group_id)
        balances = get_group_balances(connection, group_id)

        return [
            {
                "member_id": member["id"],
                "member_name": member["name"],
                "balance_cents": balances[member["id"]],
            }
            for member in members
        ]

    finally:
        connection.close()



@app.get("/api/groups/{group_id}/settlements")
def get_settlements_endpoint(group_id: int):
    connection = get_connection()

    try:
        members = list_members(connection, group_id)

        member_names = {
            member["id"]: member["name"]
            for member in members
        }

        settlements = get_group_settlements(
            connection,
            group_id,
        )

        return [
            {
                "from_member_id": settlement.from_member_id,
                "from_member_name": member_names[
                    settlement.from_member_id
                ],
                "to_member_id": settlement.to_member_id,
                "to_member_name": member_names[
                    settlement.to_member_id
                ],
                "amount_cents": settlement.amount_cents,
            }
            for settlement in settlements
        ]

    finally:
        connection.close()


@app.get("/api/groups")
def get_groups_endpoint():
    connection = get_connection()

    try:
        return list_groups(connection)

    finally:
        connection.close()



@app.get("/api/groups/{group_id}/members")
def get_members_endpoint(group_id: int):
    connection = get_connection()

    try:
        return list_members(
            connection,
            group_id,
        )

    finally:
        connection.close()



@app.get("/api/groups/{group_id}/expenses")
def get_expenses_endpoint(group_id: int):
    connection = get_connection()

    try:
        return list_expenses(
            connection,
            group_id,
        )
    finally:
        connection.close()