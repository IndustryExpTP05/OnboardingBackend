from fastapi import FastAPI
import pandas as pd

from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Path to the CSV file
CSV_FILE_PATH = "data/test.csv"

@app.get("/data")
def read_csv():
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        return df.to_dict(orient="records")  # Convert to JSON format
    except Exception as e:
        return {"error": str(e)}
