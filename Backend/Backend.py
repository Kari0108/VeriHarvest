# Role: Backend Developer
# Module: VeriHarvest Backend API (FastAPI + PostgreSQL) - to Store and Manage the Data

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Initialize FastAPI App
app = FastAPI()

# Database Connection
DATABASE_URL = "postgresql://user:password@localhost:5432/veriharvest_db"
conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
cursor = conn.cursor()

# Define Models
class FoodBatch(BaseModel):
    batch_id: int
    product_name: str
    supplier: str
    freshness_score: int
    blockchain_verified: bool
    status: str

# API Endpoints
@app.post("/add_batch/")
def add_batch(batch: FoodBatch):
    try:
        cursor.execute("INSERT INTO food_batches (batch_id, product_name, supplier, freshness_score, blockchain_verified, status) VALUES (%s, %s, %s, %s, %s, %s)",
                       (batch.batch_id, batch.product_name, batch.supplier, batch.freshness_score, batch.blockchain_verified, batch.status))
        conn.commit()
        return {"message": "Batch added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_batch/{batch_id}")
def get_batch(batch_id: int):
    cursor.execute("SELECT * FROM food_batches WHERE batch_id = %s", (batch_id,))
    batch = cursor.fetchone()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch

@app.get("/get_all_batches/")
def get_all_batches():
    cursor.execute("SELECT * FROM food_batches")
    batches = cursor.fetchall()
    return batches

# Run API Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


