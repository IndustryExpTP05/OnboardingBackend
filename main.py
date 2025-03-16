from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from database import get_db
from models import DataEntry
import pandas as pd
import asyncio
from database import create_tables

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# ✅ 1️⃣ Health Check Route
@app.get("/")
async def root():
    return {"message": "FastAPI is running on Render 🚀"}

# ✅ Run database migration at startup
@app.on_event("startup")
async def startup_event():
    await create_tables()

# ✅ 2️⃣ Check Database Connection
@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        status = result.scalar()  # ✅ Convert to a simple value instead of raw query result
        return {"database_status": f"Success: {status}"}
    except Exception as e:
        return {"error": str(e)}


# ✅ 3️⃣ Fetch Data from Database
@app.get("/check-db")
async def check_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(DataEntry))  # Fetch all records
        data = result.scalars().all()  # Convert to list

        # ✅ Serialize properly using Pydantic
        return {"database_data": [ {"id": entry.ID, "name": entry.Name} for entry in data ]}
    except Exception as e:
        return {"error": str(e)}


# ✅ 4️⃣ Insert Sample Data
@app.post("/add-sample-data")
async def add_sample_data(db: AsyncSession = Depends(get_db)):
    try:
        new_entry = DataEntry(id=1, name="Sample Name")
        db.add(new_entry)
        await db.commit()
        return {"message": "Sample data added!"}
    except Exception as e:
        return {"error": str(e)}

# ✅ 5️⃣ Fetch Data from CSV (Optional)
CSV_FILE_PATH = "data/test.csv"

@app.get("/data")
async def read_csv():
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        return df.to_dict(orient="records")  # Convert to JSON format
    except Exception as e:
        return {"error": str(e)}
