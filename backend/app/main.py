import os
from fastapi import FastAPI
import asyncpg
from pydantic import BaseModel

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "fintech")
DB_USER = os.getenv("DB_USER", "fintech_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "fintech_pass")

app = FastAPI(title="FinTech API", version="0.1.0")

@app.get("/")
async def root():
    return {"status": "ok", "service": "fintech-api"}

@app.get("/health/db")
async def db_health():
    conn = await asyncpg.connect(
        host=DB_HOST, port=DB_PORT,
        user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    try:
        val = await conn.fetchval("SELECT 1;")
        return {"db": "ok", "select_1": val}
    finally:
        await conn.close()

class Account(BaseModel):
    id: int
    owner: str
    balance: float

# Ejemplo en memoria (sin migraciones todavía)
_fake_db = {
    1: Account(id=1, owner="Alice", balance=1000.50),
    2: Account(id=2, owner="Bob", balance=250.00),
}

@app.get("/accounts/{account_id}", response_model=Account)
async def get_account(account_id: int):
    acc = _fake_db.get(account_id)
    if not acc:
        return {"detail": "not found"}
    return acc