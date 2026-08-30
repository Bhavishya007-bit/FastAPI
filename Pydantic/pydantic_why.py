from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

#Pydantic model
class Patient(BaseModel): # We have to always pass BaseModel inside the class
     #Schema defined
     name : Annotated[str, Field(max_length=20, title = 'Name of the patient', description= 'Give the name of the patient in less than 20 characters', examples= ['Amit', 'Devansh'])]
     email : EmailStr
     linkedin_url : AnyUrl
     age : int
     weight : float = Field(gt=0)
     married : bool
     allergies : Optional[List[str]] = None
     contact_details : Dict[str,str]

def insert_patient_data(patient : Patient):

    print(patient.name)
    print(patient.age)
    print('inserted')

def update_patient_data(patient : Patient):

    print(patient.name)
    print(patient.age)
    print('updated')


patient_info = {'name': 'Bhavishya', 'email':'abc@gmail.com','linkedin_url':'http://linkedin.com/1322','age':20, 'weight': 76.55, 'married': False, 'allergies': ['pollen', 'dust'], 'contact_details':{'email':'abc@gmail.com', 'phone':'789541288'}}

patient1 = Patient(**patient_info)  # Here we have used ** to unpack the dictionary

insert_patient_data(patient1)

update_patient_data(patient1)  # pydantic is smart enough and converted it into integer