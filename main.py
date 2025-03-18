from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import init_db

from router import sudoku, profile

app = FastAPI(title='sudoku',description = '',version = '1.0.0')



app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    init_db()

@app.get("/")
async def root():
    return {"message": "Sudoku"}

app.include_router(sudoku.route,prefix = '/api/v1')
app.include_router(profile.route,prefix = '/api/v1')