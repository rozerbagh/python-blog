import uvicorn
from fastapi import FastAPI
from routes import user_router
import asyncio
import platform

if platform.system() == "Darwin":
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=4000, reload=True)
