from fastapi import FastAPI
import time
import asyncio

app = FastAPI()

@app.get("/sync")
def read_sync():
	time.sleep(2)
	return {
		"message": "Synchronus blocking endpoint"
	}

@app.get("/async")
async def read_async():
	await asyncio.sleep(2)
	return {
		"message":
		"Asynchronus non-blocking endpoint"
	}
