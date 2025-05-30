from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data_service import DataService

app = FastAPI()

data_service = DataService(False)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/family")
async def root():
    return data_service.get_data()


@app.get("/max-id")
async def root():
    return data_service.get_max_id()


@app.get("/colors")
async def root():
    return data_service.get_colors()


@app.get("/cities")
async def root():
    return data_service.get_cities()

@app.post("/fields")
def check_fields(item: dict):
    return {"message": data_service.check_fields(item)}

@app.post("/update/{id}")
def create_item(id:int, item: dict):
    return {"message": data_service.update_person(id, item)}

# curl --header "Content-Type: application/json" \
#   --request POST \
#   --data '{"wedding":"marie"}' \
#   http://localhost:8000/update/0

@app.post("/parent/{id}/{gender}")
def add_parent(id:int, gender:str):
    return {"message": data_service.add_parent(id, gender)}

@app.post("/parent-visibility/{id}")
def add_parent(id:int):
    return {"message": data_service.update_parent_visibility(id)}

@app.delete("/person/{id}")
def delete(id: int):
    return {"message": data_service.delete_person(id)}
    