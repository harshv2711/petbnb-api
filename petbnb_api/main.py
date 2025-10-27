from fastapi import FastAPI
import database

app = FastAPI()

@app.get("/")
def home():
     return {
        "message":"Petbnb API"
    }

@app.get("/host")
def host():
    return {
        "message":"host api endpoint"
    }