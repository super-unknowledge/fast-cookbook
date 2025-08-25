from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
	title: str
	description: str
	status: str


class TaskWithID(Task):
	id: int


class TaskV2(BaseModel):
	title: str
	description: str
	status: str
	priority: str | None = "lower"  # FIXME: default value not applied, csv reader passes "null", default value only applied if priority field does not exist, solution is to remove empty fields after reading csv but i'm too lazy to do that


class TaskV2WithID(TaskV2):
	id: int
