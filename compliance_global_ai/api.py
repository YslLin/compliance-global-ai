from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()


class Item(BaseModel):
    file_url: str
    company_id: int


@app.post("/push")
def push(item: Item):
    return {"file_url": item.file_url, "company_id": item.company_id}
