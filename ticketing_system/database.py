from sqlalchemy import Column, Float, ForeignKey, Table
from sqlalchemy.orm import (
	DeclarativeBase,
	Mapped,
	mapped_column,
	relationship,
)


class Base(DeclarativeBase):
	pass


class Ticket(Base):
	__tablename__ = "tickets"

	id: Mapped[int] = mapped_column(primary_key=True)
	price: Mapped[float] = mapped_column(nullable=True)
	show: Mapped[str | None]
	user: Mapped[str | None]
# 	details: Mapped["TicketDetails"] = relationship(
# 		back_populates="ticket"
# 	)
	event_id: Mapped[int | None] = mapped_column(
		ForeignKey("events.id")
	)
	event: Mapped["Event | None"] = relationship(
		back_populates="tickets"
	)


class Event(Base): 
	__tablename__ = "events"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str]
	tickets: Mapped[list["Ticket"]] = relationship(
		back_populates="event"
	)
