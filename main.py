import yfinance as yf
import pandas as pd
from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stock/{symbol}/fundamental/balance-sheet")
def get_balance_sheet(symbol: str = Path(min_length=1)):
    try:
        ticker = yf.Ticker(symbol)
        balance_sheet = ticker.balance_sheet
        
        # ✅ The simplest fix: Convert to JSON string and parse back
        json_str = balance_sheet.to_json(orient='split')
        data = json.loads(json_str)
        
        return {
            "symbol": symbol,
            "data": data
        }
        
    except Exception as e:
        return {
            "symbol": symbol,
            "error": str(e)
        }