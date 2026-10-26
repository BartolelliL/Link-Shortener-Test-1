from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db
from router import router as r


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    print("Closing the application...")

app = FastAPI(lifespan=lifespan)
app.include_router(r)
