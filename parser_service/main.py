from fastapi import FastAPI
from routers import parsers

app = FastAPI()

app.include_router(parsers.router)
