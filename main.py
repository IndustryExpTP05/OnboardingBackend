from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from database import get_db
from models import DataEntry
import pandas as pd
import json
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all headers
    allow_headers=["*"],
)

# ✅ 1️⃣ Health Check Route
@app.get("/")
async def root():
    return {"message": "FastAPI is running on Render 🚀"}

# ✅ 2️⃣ API Route to Serve Cleaned JSON Data
@app.get("/cancer-data")
async def get_cancer_data():
    try:
        json_file_path = "data/cancer_data.json"  # ✅ Ensure this file exists
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return JSONResponse(content=data)  # ✅ Return JSON data
    except Exception as e:
        return {"error": str(e)}

# ✅ 3️⃣ Check Database Connection
@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        status = result.scalar()
        return {"database_status": f"Success: {status}"}
    except Exception as e:
        return {"error": str(e)}

# ✅ 4️⃣ Fetch Data from Database
@app.get("/check-db")
async def check_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(DataEntry))  # Fetch all records
        data = result.scalars().all()
        return {"database_data": [{"id": entry.id, "name": entry.name} for entry in data]}
    except Exception as e:
        return {"error": str(e)}

# ✅ 5️⃣ Optional CSV Data Fetch
CSV_FILE_PATH = "data/test.csv"

@app.get("/data")
async def read_csv():
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
