from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "MSP vCIO platform is running!"}
