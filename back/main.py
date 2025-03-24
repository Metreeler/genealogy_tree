import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


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
    # with open("data/family_reduced.json") as f:
    #     data = json.load(f)
    with open("data/family.json") as f:
        data = json.load(f)
    return data

@app.get("/colors")
async def root():
    # with open("data/colors_reduced.json") as f:
    #     data = json.load(f)
    with open("data/colors.json") as f:
        data = json.load(f)
    return data