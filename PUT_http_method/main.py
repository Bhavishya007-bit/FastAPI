from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f)

class Patient(BaseModel):

    id : Annotated[str, Field(..., description='ID of the patient', examples=['P001']) ]
    name : Annotated[str, Field(..., description='Name of the patient')]
    city : Annotated[str, Field(..., description='City where patient is living')]
    age : Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender : Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height : Annotated[float, Field(..., gt = 0, description='Height of the patient in meter')]
    weight : Annotated[float, Field(..., gt = 0, description='Weight of ther patient in kg')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)

        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal weight'
        elif self.bmi < 30:
            return 'OverWeight'
        else:
            return 'Obese'

@app.get("/")
def hello():
    return {'message': 'Patient data management system'}

@app.get("/about")
def about():
    return {
        'message': 'Hi this is my first FastAPI code thank you hehehe'
    }

@app.get('/sort')
def sort_patient(
    sort_by: str = Query(..., description='Sort on the basis of height, weight, or bmi'),
    order: str = Query('asc', description='Sort in asc or desc order')
):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f'Invalid field select from {valid_fields}'
        )

    if order not in ['asc', 'desc']:
        raise HTTPException(
            status_code=400,
            detail='Invalid order select between asc or desc'
        )

    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=sort_order
    )

    return sorted_data