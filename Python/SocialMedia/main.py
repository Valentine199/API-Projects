from fastapi import FastAPI
from fastapi import Body

#  create the instance
app = FastAPI()


# path operator or route
# If we are at this url we do this methode
@app.get("/")
# async we warn the methode that we do an asynchronous call
async def root():
    # return a JSON
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": "yOUR POST"}


@app.post("/createposts")
def create_posts(payLoad: dict = Body(...)):
    print(payLoad)
    return {"message": "Post created"}
