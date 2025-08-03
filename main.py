import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncpg
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

# Enable CORS for all
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Inventory(BaseModel):
    product_id: str
    quantity: int

db_pool: Optional[asyncpg.Pool] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_pool
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    print("✅ Connected to PostgreSQL")
    yield
    await db_pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/inventory/{product_id}")
async def get_inventory(product_id: str):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT quantity FROM inventories WHERE product_id = $1", product_id
        )
        if row is None:
            raise HTTPException(status_code=404, detail="Product not found")
        quantity = row["quantity"]
        return {"available": quantity > 0, "quantity": quantity}

@app.post("/inventory", status_code=201)
async def create_inventory(inv: Inventory):
    async with db_pool.acquire() as conn:
        try:
            await conn.execute(
                """
                INSERT INTO inventories (product_id, quantity, updated_at)
                VALUES ($1, $2, $3)
                """,
                inv.product_id, inv.quantity, datetime.utcnow()
            )
        except Exception:
            raise HTTPException(status_code=400, detail="Insert failed")
    return {"status": "created"}

@app.put("/inventory/{product_id}")
async def update_inventory(product_id: str, inv: Inventory):
    async with db_pool.acquire() as conn:
        try:
            await conn.execute(
                """
                UPDATE inventories
                SET quantity = $1, updated_at = $2
                WHERE product_id = $3
                """,
                inv.quantity, datetime.utcnow(), product_id
            )
        except Exception:
            raise HTTPException(status_code=400, detail="Update failed")
    return {"status": "updated"}
