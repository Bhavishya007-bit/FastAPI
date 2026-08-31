# Pydantic

> **Revision Notes — Pydantic with FastAPI**

Pydantic is a Python library used for **data validation, parsing, and serialization** using Python type hints.

It is especially important in **FastAPI**, where Pydantic models are commonly used to define the structure of request bodies and validate incoming data.

---

# 1. What is Pydantic?

Pydantic allows us to define an **expected schema** for our data using a Python class.

The model tells us:

- What fields should exist
- What type each field should have
- Which fields are required or optional
- What constraints the values must satisfy
- How incoming data should be converted/parsed when possible

### Simple Idea

```text
Raw Input Data
      ↓
Pydantic Model
      ↓
Validation + Parsing
      ↓
Pydantic Object
      ↓
Use safely in application
```

---

# 2. Pydantic Model

A Pydantic model is a class that inherits from `BaseModel`.

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int
    height: float
```

Here:

```text
Patient
   ↓
Pydantic Model

name    → str
age     → int
height  → float
```

The class represents the **schema** or expected structure of a patient.

---

# 3. `BaseModel`

`BaseModel` is the main class used to create Pydantic models.

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int
```

Think of `BaseModel` as the **foundation** that gives our class Pydantic's validation and parsing capabilities.

### Important

Inside a Pydantic model, fields should normally be defined using **type annotations**:

```python
name: str
age: int
weight: float
```

Not:

```python
name = str
age = int
weight = float
```

Remember:

```text
: → type annotation

= → default value
```

Example:

```python
age: int = 20
```

means:

> `age` is an integer field whose default value is `20`.

---

# 4. Creating a Pydantic Object

We can create a model object using keyword arguments:

```python
patient = Patient(
    name="Rahul",
    age=20
)
```

The variable `patient` is now a **Pydantic model object**, not just a normal dictionary.

```python
print(patient)
```

Example:

```text
name='Rahul' age=20
```

We can access fields using dot notation:

```python
print(patient.name)
print(patient.age)
```

---

# 5. Three Basic Steps

The basic workflow can be remembered as:

### Step 1 — Define the Model

```python
class Patient(BaseModel):
    name: str
    age: int
```

### Step 2 — Provide Input

```python
patient = Patient(
    name="Rahul",
    age=20
)
```

Pydantic validates the input and creates a Pydantic object.

### Step 3 — Use the Validated Object

```python
print(patient.name)
print(patient.age)
```

### Remember

```text
Define Schema
     ↓
Provide Input
     ↓
Validate + Parse
     ↓
Create Pydantic Object
     ↓
Use Validated Data
```

---

# 6. Validation

One of the main purposes of Pydantic is **data validation**.

Suppose our model expects:

```python
class Patient(BaseModel):
    name: str
    age: int
```

Valid:

```python
patient = Patient(
    name="Rahul",
    age=20
)
```

Invalid:

```python
patient = Patient(
    name="Rahul",
    age="twenty"
)
```

Pydantic raises a:

```text
ValidationError
```

### Important

```text
Valid input
    ↓
Pydantic model object

Invalid input
    ↓
ValidationError
```

---

# 7. Type Validation and Parsing

Pydantic uses Python type hints to understand the expected data type.

Example:

```python
class Patient(BaseModel):
    age: int
```

If a compatible value is supplied, Pydantic may parse/coerce it into the expected type according to its validation rules.

Example:

```python
patient = Patient(age="20")

print(patient.age)
print(type(patient.age))
```

Possible result:

```text
20
<class 'int'>
```

Therefore:

```text
Input
 ↓
Validate
 ↓
Parse / Coerce when appropriate
 ↓
Validated Model
```

---

# 8. Required Fields

A field without a default value is required.

```python
class Patient(BaseModel):
    name: str
    age: int
```

This is valid:

```python
Patient(
    name="Rahul",
    age=20
)
```

This is invalid:

```python
Patient(
    name="Rahul"
)
```

because `age` has not been provided.

---

# 9. Optional Fields

A field can be allowed to contain `None` using:

```python
int | None
```

Example:

```python
class Patient(BaseModel):
    name: str
    age: int | None = None
```

Now:

```python
patient = Patient(name="Rahul")
```

is valid.

And:

```python
patient.age
```

will be:

```text
None
```

### Older typing style

You may also see:

```python
from typing import Optional

age: Optional[int] = None
```

Modern Python allows:

```python
age: int | None = None
```

---

# 10. Field Constraints with `Field`

Pydantic allows additional validation rules using `Field`.

```python
from pydantic import BaseModel, Field

class Patient(BaseModel):
    name: str
    age: int = Field(gt=0)
```

Here:

```python
gt=0
```

means:

```text
age > 0
```

Example:

```python
Patient(name="Rahul", age=20)   # Valid
Patient(name="Rahul", age=-5)   # ValidationError
```

---

## Common Constraints

### `gt`

Greater than.

```python
age: int = Field(gt=0)
```

```text
age > 0
```

### `ge`

Greater than or equal to.

```python
age: int = Field(ge=0)
```

```text
age >= 0
```

### `lt`

Less than.

```python
age: int = Field(lt=100)
```

```text
age < 100
```

### `le`

Less than or equal to.

```python
age: int = Field(le=100)
```

```text
age <= 100
```

### `min_length`

Minimum string length.

```python
name: str = Field(min_length=3)
```

### `max_length`

Maximum string length.

```python
name: str = Field(max_length=50)
```

---

# 11. Special Pydantic Types

Pydantic provides special types for common validation requirements.

Example:

```python
from pydantic import BaseModel, EmailStr, AnyUrl

class Patient(BaseModel):
    email: EmailStr
    linkedin_url: AnyUrl
```

### `EmailStr`

Used to validate email addresses.

```python
email: EmailStr
```

Example:

```text
abc@gmail.com
```

### `AnyUrl`

Used to validate URL values.

```python
linkedin_url: AnyUrl
```

### Important

Some Pydantic features require additional dependencies.

For `EmailStr`, install:

```bash
pip install "pydantic[email]"
```

---

# 12. `ValidationError`

When input doesn't satisfy the model, Pydantic raises `ValidationError`.

```python
from pydantic import BaseModel, ValidationError

class Patient(BaseModel):
    name: str
    age: int

try:
    patient = Patient(
        name="Rahul",
        age="abc"
    )
except ValidationError as e:
    print(e)
```

### Remember

```text
Wrong Input
    ↓
Pydantic Validation
    ↓
ValidationError
```

---

# 13. Dictionary → Pydantic Object

Suppose we have:

```python
patient_info = {
    "name": "Rahul",
    "age": 20
}
```

We can create a Pydantic object using:

```python
patient = Patient(**patient_info)
```

### What does `**` do?

It **unpacks a dictionary**.

This:

```python
Patient(**patient_info)
```

is conceptually similar to:

```python
Patient(
    name="Rahul",
    age=20
)
```

In Pydantic v2, another important approach is:

```python
patient = Patient.model_validate(patient_info)
```

---

# 14. Nested Models

A Pydantic model can contain another Pydantic model.

This is called a **Nested Model**.

Example:

```python
from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str


class Patient(BaseModel):

    name: str
    age: int
    gender: str
    address: Address
```

Here:

```python
address: Address
```

means that the `address` field itself follows the `Address` Pydantic model.

---

## Creating the Nested Model

First create the address:

```python
address_dict = {
    'city': 'Faridabad',
    'state': 'Haryana',
    'pin': '121001'
}

address1 = Address(**address_dict)
```

Then use it inside `Patient`:

```python
patient_dict = {
    'name': 'Bhavishya Gaur',
    'age': '22',
    'gender': 'male',
    'address': address1
}

patient1 = Patient(**patient_dict)
```

### Structure

```text
Patient
│
├── name
├── age
├── gender
│
└── address
      │
      ├── city
      ├── state
      └── pin
```

---

## Accessing Nested Fields

```python
print(patient1.name)
print(patient1.age)
print(patient1.gender)

print(patient1.address)

print(patient1.address.city)
print(patient1.address.state)
```

Notice:

```python
patient1.address.city
```

We first access:

```text
patient1
   ↓
address
   ↓
city
```

---

## Nested Dictionary Input

Pydantic can also work with nested dictionaries directly.

For example:

```python
patient1 = Patient(
    name="Bhavishya Gaur",
    age=22,
    gender="male",
    address={
        "city": "Faridabad",
        "state": "Haryana",
        "pin": "121001"
    }
)
```

Pydantic validates the nested `address` according to the `Address` model.

---

# 15. Serialization

## What is Serialization?

Serialization means converting a Pydantic model into a format that can easily be:

- Stored
- Transmitted
- Returned from an API
- Converted into JSON

A common flow is:

```text
Pydantic Object
      ↓
Serialization
      ↓
Dictionary / JSON
```

---

# 16. `model_dump()`

In Pydantic v2:

```python
patient1.model_dump()
```

converts a Pydantic model into a Python dictionary.

Example:

```python
temp = patient1.model_dump()

print(temp)
```

Conceptually:

```text
Pydantic Object
      ↓
model_dump()
      ↓
Python Dictionary
```

Example output:

```python
{
    "name": "Bhavishya Gaur",
    "age": 22,
    "gender": "male",
    "address": {
        "city": "Faridabad",
        "state": "Haryana",
        "pin": "121001"
    }
}
```

Notice that the nested model is also represented as a dictionary.

---

# 17. `model_dump_json()`

If we want a JSON representation:

```python
temp1 = patient1.model_dump_json()

print(temp1)
```

Flow:

```text
Pydantic Object
      ↓
model_dump_json()
      ↓
JSON String
```

### Important Difference

```python
model_dump()
```

returns a:

```text
Python dictionary
```

while:

```python
model_dump_json()
```

returns:

```text
JSON representation as a string
```

---

# 18. Serialization Example

```python
from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str


class Patient(BaseModel):

    name: str
    age: int
    gender: str
    address: Address


address_dict = {
    'city': 'Faridabad',
    'state': 'Haryana',
    'pin': '121001'
}

address1 = Address(**address_dict)

patient_dict = {
    'name': 'Bhavishya Gaur',
    'age': '22',
    'gender': 'male',
    'address': address1
}

patient1 = Patient(**patient_dict)


# Pydantic object → Dictionary
temp = patient1.model_dump()

# Pydantic object → JSON
temp1 = patient1.model_dump_json()

print(temp)
print(temp1)
```

---

# 19. Computed Fields

A **computed field** is a field whose value is calculated from other fields rather than directly supplied as input.

Example:

```python
from pydantic import BaseModel, computed_field

class Patient(BaseModel):

    weight: float
    height: float

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
```

Here:

```python
weight
height
```

are actual input fields.

But:

```python
bmi
```

is calculated from them.

---

## Why Use Computed Fields?

Suppose:

```python
weight = 76.55
height = 1.8
```

Instead of asking the user to provide:

```python
bmi = 23.62
```

we can calculate it:

```python
bmi = weight / height²
```

This avoids asking the user for information that can be derived from existing data.

---

# 20. `@computed_field` and `@property`

A typical computed field is written as:

```python
@computed_field
@property
def bmi(self) -> float:
    return self.weight / (self.height ** 2)
```

### `@property`

Allows us to access the method like an attribute:

```python
patient.bmi
```

instead of:

```python
patient.bmi()
```

### `@computed_field`

Tells Pydantic that this calculated property should be treated as a computed field and included in relevant serialization/schema behavior.

---

# 21. Computed Field Example — BMI

```python
from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict


class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int

    weight: float  # kg
    height: float  # metres

    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]


    @computed_field
    @property
    def bmi(self) -> float:

        bmi = self.weight / (self.height ** 2)

        return bmi
```

Now:

```python
patient1 = Patient(
    name="Bhavishya",
    email="abc@hdfc.com",
    age="20",
    weight=76.55,
    height=1.8,
    married=False,
    allergies=["pollen", "dust"],
    contact_details={
        "emergency": "abc@gmail.com",
        "phone": "789541288"
    }
)
```

We can access:

```python
print(patient1.bmi)
```

without providing `bmi` during object creation.

---

# 22. Important Computed Field Concept

Think of it like this:

```text
User Input
   │
   ├── weight = 76.55
   └── height = 1.8
            │
            ↓
      Computed Field
            │
            ↓
          BMI
```

So:

```text
Input Field
→ Provided by user

Computed Field
→ Derived/calculated from existing data
```

---

# 23. Field Validators

A **field validator** allows us to write custom validation logic for a particular field.

Example:

```python
from pydantic import BaseModel, EmailStr, field_validator

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        valid_domains = [
            'hdfc.com',
            'icici.com'
        ]

        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return value
```

Here the validator applies specifically to:

```python
email
```

---

# 24. Why Use `field_validator`?

Pydantic already performs basic validation.

For example:

```python
email: EmailStr
```

checks whether the value is a valid email address.

But suppose our application has an additional business rule:

> Only `hdfc.com` and `icici.com` emails are allowed.

Pydantic doesn't automatically know this business rule.

So we add:

```python
@field_validator('email')
```

---

# 25. Field Validator Example

```python
@field_validator('email')
@classmethod
def email_validator(cls, value):

    valid_domains = [
        'hdfc.com',
        'icici.com'
    ]

    domain_name = value.split('@')[-1]

    if domain_name not in valid_domains:
        raise ValueError('Not a valid domain')

    return value
```

For:

```text
abc@hdfc.com
```

the domain is:

```text
hdfc.com
```

Therefore it is valid.

For:

```text
abc@gmail.com
```

the domain is:

```text
gmail.com
```

which isn't in:

```python
['hdfc.com', 'icici.com']
```

so:

```python
ValueError
```

is raised.

---

# 26. Field Validator for Age

We can also validate an integer field.

```python
@field_validator('age', mode='after')
@classmethod
def validate_age(cls, value):

    if 0 < value < 100:
        return value

    else:
        raise ValueError(
            'Age should be in between 0 to 100'
        )
```

This means:

```text
0 < age < 100
```

is required.

Valid:

```text
20
50
99
```

Invalid:

```text
0
100
150
-5
```

---

# 27. `mode='after'`

Consider:

```python
@field_validator('age', mode='after')
```

`mode='after'` means the validator runs **after Pydantic's normal validation/parsing for that field**.

For example:

```python
age = "20"
```

Pydantic can first parse it to:

```python
20
```

Then our validator receives the parsed value.

Conceptually:

```text
Input
 ↓
"20"
 ↓
Pydantic parsing
 ↓
20 (int)
 ↓
field_validator(mode="after")
 ↓
Check age range
```

This is why `mode='after'` is useful when your custom validation expects the value to already have its declared type.

---

# 28. `mode='before'`

A field validator can also run before Pydantic's normal validation.

```python
@field_validator('age', mode='before')
@classmethod
def validate_age(cls, value):
    ...
```

Conceptually:

```text
Input
 ↓
field_validator(mode="before")
 ↓
Pydantic validation/parsing
 ↓
Final field value
```

### Important

`before` receives the **raw input value**.

`after` receives the value after Pydantic has performed its normal validation/parsing.

```text
             Input
               │
               ↓
        ┌──────────────┐
        │    BEFORE    │
        │   validator  │
        └──────┬───────┘
               ↓
       Pydantic validation
               ↓
        ┌──────────────┐
        │    AFTER     │
        │   validator  │
        └──────────────┘
```

---

# 29. Why `before` Can Be Useful

Suppose we want to clean or transform raw input before Pydantic processes it.

Example:

```python
@field_validator('name', mode='before')
@classmethod
def clean_name(cls, value):

    if isinstance(value, str):
        return value.strip()

    return value
```

Here the raw input is modified before normal Pydantic validation.

### Easy way to remember

```text
before
→ Work with raw input

after
→ Work with validated/parsed value
```

---

# 30. `@classmethod` in Field Validators

You will commonly see:

```python
@field_validator('age')
@classmethod
def validate_age(cls, value):
    ...
```

The validator is defined as a class method.

The important part for revision is to remember the general structure:

```python
@field_validator('field_name')
@classmethod
def validator_name(cls, value):
    ...
    return value
```

The validator should normally return the value after validating or transforming it.

---

# 31. Model Validators

A **model validator** validates the model as a whole rather than focusing on just one field.

Use it when the validation rule depends on **multiple fields together**.

Example:

```python
from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict


class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]


    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):

        if (
            model.age > 60
            and 'emergency' not in model.contact_details
        ):
            raise ValueError(
                'Patients older than 60 must have '
                'an emergency contact'
            )

        return model
```

---

# 32. Why Use `model_validator`?

Look at the rule:

> If the patient is older than 60, they must have an emergency contact.

This rule depends on:

```text
age
+
contact_details
```

Therefore, validating only one field isn't enough.

We need to look at the **relationship between multiple fields**.

That's where `model_validator` is useful.

---

# 33. Model Validator — Flow

```text
Patient Input
     │
     ├── age
     │
     ├── contact_details
     │
     └── other fields
            │
            ↓
     Model Validation
            │
            ↓
     Check relationship
            │
       ┌────┴────┐
       ↓         ↓
    Valid      Invalid
       ↓         ↓
 Return model  ValueError
```

---

# 34. `mode='after'` for Model Validator

Your example uses:

```python
@model_validator(mode='after')
```

This means the model-level validation occurs after the model has been validated/constructed.

Therefore, inside the validator we can work with the model:

```python
model.age
model.contact_details
```

Example:

```python
if model.age > 60 and 'emergency' not in model.contact_details:
    raise ValueError(
        'Patients older than 60 must have an emergency contact'
    )
```

---

# 35. Field Validator vs Model Validator

This distinction is **very important**.

| Feature | `field_validator` | `model_validator` |
|---|---|---|
| Scope | One or more selected fields | Whole model |
| Main purpose | Validate a field | Validate relationships between fields |
| Example | Validate email domain | Age + emergency contact |
| Access | Field value | Whole model |
| Typical use | Email, age, name | Cross-field/business rules |

### Easy Memory Trick

```text
FIELD validator
      ↓
"Is THIS field valid?"

MODEL validator
      ↓
"Is THIS COMBINATION of fields valid?"
```

---

# 36. Example Comparison

### Field Validator

```python
@field_validator('age')
@classmethod
def validate_age(cls, value):

    if 0 < value < 100:
        return value

    raise ValueError('Invalid age')
```

Question being asked:

```text
"Is the AGE valid?"
```

---

### Model Validator

```python
@model_validator(mode='after')
def validate_emergency_contact(cls, model):

    if model.age > 60 and 'emergency' not in model.contact_details:
        raise ValueError(
            'Patients older than 60 must have an emergency contact'
        )

    return model
```

Question being asked:

```text
"Given the patient's AGE,
does the CONTACT INFORMATION satisfy the rule?"
```

---

# 37. Serialization + Nested Models

Nested models and serialization work together.

Suppose:

```python
class Address(BaseModel):
    city: str
    state: str
    pin: str


class Patient(BaseModel):
    name: str
    age: int
    address: Address
```

Then:

```python
patient.model_dump()
```

produces a dictionary containing a nested dictionary:

```python
{
    "name": "Bhavishya",
    "age": 22,
    "address": {
        "city": "Faridabad",
        "state": "Haryana",
        "pin": "121001"
    }
}
```

So:

```text
Nested Pydantic Object
        ↓
model_dump()
        ↓
Nested Dictionary
```

---

# 38. Pydantic with FastAPI

Pydantic is deeply integrated with FastAPI.

A Pydantic model can define the structure of a request body.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Patient(BaseModel):
    name: str
    age: int
    weight: float


@app.post("/patient")
def create_patient(patient: Patient):

    return patient
```

A client can send:

```json
{
    "name": "Rahul",
    "age": 20,
    "weight": 65.5
}
```

FastAPI:

```text
JSON Request
     ↓
Pydantic Model
     ↓
Validation
     ↓
Patient Object
     ↓
FastAPI Function
```

If the request doesn't satisfy the model, FastAPI automatically generates a validation error response.

---

# 39. Path / Query Parameters vs Request Body

### Path Parameter

```python
@app.get("/patient/{patient_id}")
def get_patient(patient_id: str):
    ...
```

Example:

```text
/patient/P001
```

Used to identify a particular resource.

---

### Query Parameter

```python
@app.get("/patients")
def get_patients(age: int | None = None):
    ...
```

Example:

```text
/patients?age=20
```

Used for things such as:

- Filtering
- Searching
- Sorting
- Pagination

---

### Request Body

```python
@app.post("/patient")
def create_patient(patient: Patient):
    ...
```

Example:

```json
{
    "name": "Rahul",
    "age": 20
}
```

### Easy Way to Remember

```text
Path Parameter
    ↓
/patient/P001
    ↓
WHICH resource?

Query Parameter
    ↓
/patients?age=20
    ↓
HOW do I filter/control the result?

Request Body
    ↓
JSON data
    ↓
WHAT data am I sending?
```

---

# 40. Important Pydantic v2 Methods

| Method | Purpose |
|---|---|
| `model_validate()` | Validate input and create a model |
| `model_validate_json()` | Validate JSON input |
| `model_dump()` | Convert model to dictionary |
| `model_dump_json()` | Convert model to JSON |

Example:

```python
data = {
    "name": "Rahul",
    "age": 20
}

patient = Patient.model_validate(data)

data = patient.model_dump()

json_data = patient.model_dump_json()
```

### Pydantic v1 vs v2

You may see older tutorials using:

```python
patient.dict()
patient.json()
```

In Pydantic v2, the preferred methods are:

```python
patient.model_dump()
patient.model_dump_json()
```

---

# 41. Pydantic vs Dictionary

A dictionary is flexible:

```python
patient = {
    "name": "Rahul",
    "age": 20
}
```

But the dictionary itself does not define a validation schema.

A Pydantic model defines:

```python
class Patient(BaseModel):
    name: str
    age: int
```

So:

```text
Dictionary
→ Flexible data structure

Pydantic Model
→ Structured + validated data
```

---

# 42. Pydantic vs Normal Python Class

### Normal Python Class

```python
class Patient:

    def __init__(self, name, age):
        self.name = name
        self.age = age
```

Python does not automatically enforce:

```text
name must be str
age must be int
age must be > 0
```

### Pydantic Model

```python
class Patient(BaseModel):

    name: str
    age: int = Field(gt=0)
```

Pydantic provides:

- Validation
- Parsing
- Structured data
- Serialization
- Custom validators

---

# 43. Complete Validation Flow

Once you have learned validators, the overall concept can be visualized as:

```text
                     RAW INPUT
                         │
                         ↓
              ┌─────────────────────┐
              │ Field Validator     │
              │ mode="before"       │
              │                     │
              │ Raw input           │
              └──────────┬──────────┘
                         ↓
              Pydantic Type Validation
                    + Parsing
                         │
                         ↓
              ┌─────────────────────┐
              │ Field Validator     │
              │ mode="after"        │
              │                     │
              │ Parsed field value  │
              └──────────┬──────────┘
                         ↓
                Pydantic Model
                         │
                         ↓
              ┌─────────────────────┐
              │ Model Validator     │
              │ mode="after"        │
              │                     │
              │ Whole model         │
              └──────────┬──────────┘
                         ↓
                  Valid Model
                         │
                         ↓
               Application Logic
                         │
                         ↓
                  Serialization
                  /            \
                 ↓              ↓
          Dictionary           JSON
```

> **Note:** The exact validation ordering can become more detailed when multiple validators, different modes, and nested models are involved. The diagram above is a conceptual revision model.

---

# 44. Key Terms to Remember

### Schema

The expected structure of data.

```text
Patient
├── name → str
├── age → int
├── weight → float
└── height → float
```

### Validation

Checking whether input satisfies defined rules.

### Parsing / Coercion

Converting compatible input into the expected representation when Pydantic's rules allow it.

### Pydantic Model

A Python class derived from `BaseModel` that defines and validates a data schema.

### Pydantic Object

An instance created from a Pydantic model.

### Nested Model

A Pydantic model used as a field inside another Pydantic model.

### Serialization

Converting a Pydantic object into a dictionary or JSON representation.

### Computed Field

A field calculated from existing model data.

### Field Validator

Custom validation logic applied to a field.

### Model Validator

Custom validation logic applied to the model as a whole.

### ValidationError

The error raised when input fails validation.

---

# 45. One-Line Revision Notes

```text
Pydantic
→ Data validation, parsing and serialization library.

BaseModel
→ Base class used to create Pydantic models.

Field()
→ Adds constraints and metadata to fields.

EmailStr
→ Validates email addresses.

AnyUrl
→ Validates URL values.

ValidationError
→ Raised when input fails validation.

Nested Model
→ One Pydantic model inside another.

model_validate()
→ Validates input and creates a model.

model_dump()
→ Converts model to a dictionary.

model_dump_json()
→ Converts model to JSON.

computed_field
→ Makes a calculated property part of the Pydantic model's
  computed-field/serialization behavior.

field_validator
→ Custom validation for a particular field.

field_validator(mode="before")
→ Runs before normal field validation/parsing.

field_validator(mode="after")
→ Runs after normal field validation/parsing.

model_validator
→ Validates the model as a whole.

model_validator(mode="after")
→ Runs model-level validation after model validation/construction.
```

---

# 46. Most Important Mental Model

If you remember only one thing, remember this:

```text
                         PYDANTIC
                            │
                            ↓
                     Define Schema
                            │
                            ↓
                      BaseModel
                            │
                            ↓
                 Fields + Type Hints
                            │
                            ↓
                    Field Constraints
                         (Field)
                            │
                            ↓
                      Raw Input
                            │
              ┌─────────────┴─────────────┐
              ↓                           ↓
       Field Validator              Normal Validation
        mode="before"                      │
              │                            ↓
              └──────────────→ Parsed Field
                                           │
                                           ↓
                                  Field Validator
                                   mode="after"
                                           │
                                           ↓
                                    Complete Model
                                           │
                                           ↓
                                   Model Validator
                                           │
                                           ↓
                                    Valid Model
                                           │
                         ┌─────────────────┴─────────────────┐
                         ↓                                   ↓
                  Application Logic                    Serialization
                                                             │
                                                     ┌───────┴───────┐
                                                     ↓               ↓
                                                  Dictionary        JSON
```

---

# 47. Final Cheat Sheet

```text
                    PYDANTIC CHEAT SHEET

┌─────────────────────────────────────────────────────────┐
│ BaseModel                                               │
│ → Create Pydantic models                                │
├─────────────────────────────────────────────────────────┤
│ Type Annotations                                        │
│ → Define expected types                                 │
│                                                         │
│ name: str                                               │
│ age: int                                                │
├─────────────────────────────────────────────────────────┤
│ Field()                                                 │
│ → Add constraints                                       │
│                                                         │
│ age: int = Field(gt=0)                                  │
├─────────────────────────────────────────────────────────┤
│ Nested Model                                            │
│ → Model inside another model                            │
│                                                         │
│ address: Address                                        │
├─────────────────────────────────────────────────────────┤
│ field_validator                                         │
│ → Validate one field                                    │
│                                                         │
│ "Is THIS field valid?"                                  │
├─────────────────────────────────────────────────────────┤
│ model_validator                                         │
│ → Validate multiple fields/model relationships          │
│                                                         │
│ "Is THIS combination of fields valid?"                 │
├─────────────────────────────────────────────────────────┤
│ computed_field                                          │
│ → Calculate a field from existing data                  │
│                                                         │
│ BMI = weight / height²                                  │
├─────────────────────────────────────────────────────────┤
│ model_dump()                                            │
│ → Model → Dictionary                                    │
├─────────────────────────────────────────────────────────┤
│ model_dump_json()                                       │
│ → Model → JSON                                          │
├─────────────────────────────────────────────────────────┤
│ model_validate()                                        │
│ → Input → Validated Model                               │
└─────────────────────────────────────────────────────────┘
```

---

# 48. Final Conceptual Picture

```text
                    CLIENT / USER
                         │
                         ↓
                      JSON DATA
                         │
                         ↓
                  ┌──────────────┐
                  │   PYDANTIC   │
                  │              │
                  │   Schema     │
                  │   Types      │
                  │   Fields     │
                  │   Validators │
                  └──────┬───────┘
                         │
                         ↓
                     VALIDATION
                         │
                ┌────────┴────────┐
                ↓                 ↓
             VALID             INVALID
                ↓                 ↓
         Pydantic Object     ValidationError
                │
                ↓
         Application Logic
                │
                ↓
          Computed Fields
                │
                ↓
           Serialization
                │
          ┌─────┴─────┐
          ↓           ↓
      Dictionary      JSON
```

> **Core Idea:** Pydantic lets you define what your data **should look like**, validates and parses incoming data according to that schema, allows custom field/model validation, supports derived computed values and nested structures, and provides tools to serialize validated models into dictionary or JSON representations.