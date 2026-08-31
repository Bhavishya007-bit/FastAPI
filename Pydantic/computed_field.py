# Computed field is that field of the model not provided by the user

from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict

#Pydantic model
class Patient(BaseModel): # We have to always pass BaseModel inside the class
     #Schema defined
     name : str
     email : EmailStr
     age : int
     weight : float
     married : bool
     allergies : List[str]
     contact_details : Dict[str, str]



     
def insert_patient_data(patient : Patient):

    print(patient.name)
    print(patient.age)
    print('inserted')

def update_patient_data(patient : Patient):

    print(patient.name)
    print(patient.age)
    print('updated')


patient_info = {'name': 'Bhavishya', 'email':'abc@hdfc.com','linkedin_url':'http://linkedin.com/1322','age':'200', 'weight': 76.55, 'married': False, 'allergies': ['pollen', 'dust'], 'contact_details':{'emergency':'abc@gmail.com', 'phone':'789541288'}}

patient1 = Patient(**patient_info)  # Here we have used ** to unpack the dictionary

insert_patient_data(patient1)

update_patient_data(patient1)  # pydantic is smart enough and converted it into integer

# fieldvalidator 'before' take value before the coersive