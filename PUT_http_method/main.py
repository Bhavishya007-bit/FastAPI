from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Annotated, Literal
import json

app = FastAPI()

def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)

    return data

class Patient(BaseModel):

    id : Annotated[str, Field(..., description='ID of the patient', examples=['P001']) ]
    name : Annotated[str, Field(..., description='Name of the patient')]
    city : Annotated[str, Field(..., description='City where patient is living')]
    age : Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender : Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height : Annotated[float, Field(..., gt = 0, description='Height of the patient in meter')]
    weight : Annotated[float, Field(..., gt = 0, description='Weight of ther patient in kg')]
    