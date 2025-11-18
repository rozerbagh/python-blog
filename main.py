import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import platform
from middleware import register_middlewares
from routes import user_router, auth_router

if platform.system() == "Darwin":
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
app = FastAPI(title="Blog API with Middleware")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)
register_middlewares(app)
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

app.include_router(user_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=4000, reload=True)
