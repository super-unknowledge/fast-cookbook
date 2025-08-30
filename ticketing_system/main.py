from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base
from db_connection import (
	AsyncSessionLocal,
	get_db_session,
	get_engine,
)
from operations import create_ticket

@asynccontextmanager
async def lifespan(app: FastAPI):
	engine = get_engine()
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
		yield
	await engine.dispose()


app = FastAPI(lifespan=lifespan)


class TicketRequest(BaseModel):
	price: float | None
	show: str | None
	user: str | None


@app.post("/ticket", response_model=dict[str, int])
async def create_ticket_route(
	ticket: TicketRequest,
	db_session: Annotated[
		AsyncSession,
		Depends(get_db_session)
	]
):
	ticket_id = await create_ticket(
		db_session,
		ticket.show,
		ticket.user,
		ticket.price,
	)
	return {"ticket_id": ticket_id}
