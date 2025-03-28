from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data_service import DataService

app = FastAPI()
    
data_service = DataService(True)

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


@app.post("/update")
def create_item(item: dict):
    return {"message": data_service.update_person(item)}

@app.post("/parent/{id}")
def add_parent(id:int, item:dict):
    return {"message": data_service.add_parent(id, item)}

@app.delete("/person/{id}")
def delete(id: int):
    return {"message": data_service.delete_person(id)}
    