from fastapi import FastAPI


app = FastAPI()

@app.get("/life")
def life():
    return {"message": "Hello World"}