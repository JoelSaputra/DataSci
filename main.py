import yfinance as yf
import pandas as pd
from fastapi import FastAPI, HTTPException, Path, status
from typing import Optional 
from pydantic import BaseModel

msft = yf.Ticker("MSFT")

users = {1:
         { 
             "name":"Joel",
             "age":"20"
          }
         }

class User(BaseModel):
    name: str
    age : int 


class UpdateUser(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None


app = FastAPI()

@app.get("/")
def root():
    return {"Hello" : "World"}


@app.get("/users/{user_id}")
def get_user(user_id: int = Path(..., description="The ID you want to get", gt=0, lt=1000)):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]
    

@app.post("/users/{user_id}", status_code=status.HTTP_201_CREATED)
def create_user(user_id:int, user:User):
    if user_id in users:
        raise HTTPException(status_code=400, detail ="User already exists")

    else:
        users[user_id] = user.model_dump()
        return user
        
@app.put("/users/{user_id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id:int, user:UpdateUser):
    if user_id not in users:
        raise HTTPException(status_code=400, detail ="User already exists")
    
    current_user = users[user_id]

    if user.name is not None: 
        current_user["name"] = user.name
    if user.age is not None:
        current_user["age"] = user.age

    return current_user


#Test P/E ratio vs 5 Year Average
#P/E = Stock Price / EPS

@app.get("/stocks/testPE")
def peTest():
    prices = msft.history(period="5y")
    eps = msft.financials.loc["Diluted EPS"]
    print(prices["Close"])
    print(eps)
    
    return {
        "prices": prices["Close"].to_dict(), 
        "eps" : eps.to_dict()    
        }
