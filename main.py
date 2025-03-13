from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Health check route
@app.get("/")
async def root():
    return {"message": "FastAPI is running on Render 🚀"}

# ✅ Check database connection
@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute("SELECT 1")
        return {"database_status": result.fetchall()}
    except Exception as e:
        return {"error": str(e)}

# ✅ Example CSV reading route (if needed)
import pandas as pd

CSV_FILE_PATH = "data/test.csv"

@app.get("/data")
async def read_csv():
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        return df.to_dict(orient="records")  # Convert to JSON format
    except Exception as e:
        return {"error": str(e)}
