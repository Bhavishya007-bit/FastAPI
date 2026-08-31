# Now how to import our pydantic model as JSON or Dictionary

from pydantic import BaseModel

class Address(BaseModel):

    city : str
    state : str
    pin : str

class Patient(BaseModel):

    name : str
    age : int
    gender : str
    address : Address


address_dict = {'city' : 'faridabad', 'state' : 'haryana', 'pin':'121001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'bhavishya gaur', 'age':'22', 'gender':'male', 'address': address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump()
temp1 = patient1.model_dump_json()

print(temp)
print(temp1)