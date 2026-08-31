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

print(patient1.name)
print(patient1.age)
print(patient1.gender)
print(patient1.address)
print(patient1.address.city)
print(patient1.address.state)