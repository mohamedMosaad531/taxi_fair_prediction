from fastapi import FastAPI
import uvicorn

app=FastAPI()

@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get('/Welcome')
def get_name(name:str):
    return {f'Welcome to {name}'}


if __name__=="__main__":
    uvicorn.run(app, reload=True)


