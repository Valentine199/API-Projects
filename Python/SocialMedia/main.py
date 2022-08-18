from fastapi import FastAPI

#  create the instance
app = FastAPI()


# path operator or route
# If we are at this url we do this methode
@app.get("/")
# async we warn the methode that we do an asynchronous call
async def root():
    # return a JSON
    return {"message": "Welcome!!"}
