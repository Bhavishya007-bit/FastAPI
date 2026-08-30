from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

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

     @field_validator('email')
     @classmethod
     def email_validator(cls, value):

         valid_domains = ['hdfc.com', 'icici.com']

         domain_name = value.split('@')[-1]

         if domain_name not in valid_domains:
             raise ValueError('Not a valid domain')
         return value

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