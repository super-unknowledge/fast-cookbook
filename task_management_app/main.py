from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from security import (
	User,
	UserInDB,
	fake_token_generator,
	fakely_hash_password,
	fake_users_db,
	get_user_from_token
)
from models import Task, TaskWithID
from models import TaskV2, TaskV2WithID
from operations import read_all_tasks, create_task, modify_task, remove_task, read_task, read_all_tasks_v2
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.post("/token")
async def login(
	form_data: OAuth2PasswordRequestForm = Depends(),
):
	user_dict = fake_users_db.get(form_data.username)
	if not user_dict:
		raise HTTPException(
			status_code=400,
			detail="Incorrect username or password",
		)
	user = UserInDB(**user_dict)
	hashed_password = fakely_hash_password(
		form_data.password
	)
	if not hashed_password == user.hashed_password:
		raise HTTPException(
			status_code=400,
			detail="Incorrect username or password",
		)

	token = fake_token_generator(user)

	return {
		"access_token": token,
		"token_type": "bearer"
	}


@app.get("/users/me", response_model=User)
def read_users_me(
	current_user: User = Depends(get_user_from_token),
):
	return current_user


@app.get("/tasks/search", response_model=list[TaskWithID])
def search_tasks(keyword: str):
	tasks = read_all_tasks()
	filtered_tasks = [
		task
		for task in tasks
		if keyword.lower()
		in (task.title + task.description).lower()
	]
	return filtered_tasks


@app.get("/v2/tasks", response_model=list[TaskV2WithID])
def get_tasks_v2():
	tasks = read_all_tasks_v2()
	for task in tasks:
		print(task)
	return tasks


@app.get("/tasks", response_model=list[TaskWithID])
def get_tasks(
	status: Optional[str] = None,
	title: Optional[str] = None,
):
	tasks = read_all_tasks()
	if status:
		tasks = [
			task
			for task in tasks
			if task.status == status
		]
	if title:
		tasks = [
			task for task in tasks if task.title == title
		]
	return tasks


@app.get("/task/{task_id}")
def get_task(task_id: int):
	task = read_task(task_id)
	if not task:
		raise HTTPException(
			status_code=404, detail="task not found"
		)
	return task


@app.post("/task", response_model=TaskWithID)
def add_task(task: Task):
	return create_task(task)


class UpdateTask(BaseModel):
	title: str | None = None
	description: str | None = None
	status: str | None = None

@app.put("/task/{task_id}", response_model=TaskWithID)
def update_task(
	task_id: int, task_update: UpdateTask
):
	modified = modify_task(
		task_id,
		task_update.model_dump(exclude_unset=True),
	)
	if not modified:
		raise HTTPException(
			status_code=404, detail="task not found"
		)

	return modified


@app.delete("/task/{task_id}", response_model=Task)
def delete_task(task_id: int):
	removed_task = remove_task(task_id)
	if not removed_task:
		raise HTTPException(
			status_code=404, detail="task not found"
		)
	return removed_task
