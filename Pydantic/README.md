# Pydantic

> **Revision Notes — Pydantic with FastAPI**

Pydantic is a Python library used for **data validation, parsing, and serialization** using Python type hints.

It is especially important in **FastAPI**, where Pydantic models are commonly used to define the structure of request bodies and validate incoming data.

---

## 1. What is Pydantic?

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

The class represents the **ideal schema** or expected structure of a patient.

---

# 3. Three Basic Steps

The basic workflow can be remembered as:

### Step 1 — Define the Model

Define the expected fields, types, and constraints.

```python
class Patient(BaseModel):
    name: str
    age: int
    height: float
```

### Step 2 — Create / Validate an Object

Provide raw input data to the model.

```python
patient = Patient(
    name="Rahul",
    age=20,
    height=175.5
)
```

Pydantic validates the input and creates a **Pydantic model object**.

### Step 3 — Use the Validated Object

The validated object can then be passed to functions or used throughout the application.

```python
print(patient.name)
print(patient.age)
```

### Remember

```text
Define Schema
     ↓
Validate Input
     ↓
Create Pydantic Object
     ↓
Use Validated Data
```

---

# 4. `BaseModel`

`BaseModel` is the main class used to create Pydantic models.

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int
```

Think of `BaseModel` as the **foundation** that gives our class Pydantic's validation and parsing capabilities.

---

# 5. Creating a Pydantic Object

We can create a model object using keyword arguments:

```python
patient = Patient(
    name="Rahul",
    age=20
)
```

The variable `patient` is now a **Pydantic object**, not just a normal dictionary.

```python
print(patient)
```

Example output:

```text
name='Rahul' age=20
```

We can access individual fields using dot notation:

```python
print(patient.name)
print(patient.age)
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

Then:

```python
patient = Patient(
    name="Rahul",
    age=20
)
```

is valid.

But invalid data can cause a validation error:

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

For example:

```python
class Patient(BaseModel):
    age: int
```

If a compatible value is supplied, Pydantic may parse/coerce it into the expected type depending on the field and validation configuration.

For example:

```python
patient = Patient(age="20")

print(patient.age)
print(type(patient.age))
```

The resulting value can be parsed as:

```text
20
<class 'int'>
```

### Important Distinction

Pydantic is not simply checking:

> "Is this value already exactly the correct Python type?"

It performs **validation and parsing/coercion** according to Pydantic's rules.

Therefore, always think:

```text
Input
 ↓
Validate
 ↓
Parse/coerce when appropriate
 ↓
Validated model
```

---

# 8. Required Fields

By default, a field without a default value is required.

```python
class Patient(BaseModel):
    name: str
    age: int
```

Both fields are required.

This is valid:

```python
Patient(name="Rahul", age=20)
```

This is invalid:

```python
Patient(name="Rahul")
```

because `age` has not been provided.

---

# 9. Optional Fields

A field can be allowed to contain `None` using:

```python
str | None
```

Example:

```python
class Patient(BaseModel):
    name: str
    age: int | None = None
```

Now `age` can be omitted:

```python
patient = Patient(name="Rahul")
```

and:

```python
patient.age
```

will be:

```text
None
```

### Important

These two ideas are related but not identical:

```python
age: int | None
```

means the value may be `int` or `None`.

```python
age: int | None = None
```

also gives the field a default of `None`, making it optional to provide.

---

# 10. Field Constraints with `Field`

Pydantic allows us to put additional validation rules on fields.

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

> `age` must be **greater than 0**.

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

# 11. Example: Patient Model with Validation

```python
from pydantic import BaseModel, Field

class Patient(BaseModel):
    name: str
    age: int = Field(gt=0)
    weight: float = Field(gt=0)
    height: float = Field(gt=0)
```

This model describes a patient with:

```text
name
 ↓
string

age
 ↓
integer > 0

weight
 ↓
float > 0

height
 ↓
float > 0
```

Example:

```python
patient = Patient(
    name="Rahul",
    age=20,
    weight=65.5,
    height=175
)
```

---

# 12. `ValidationError`

When the input does not satisfy the model, Pydantic raises `ValidationError`.

```python
from pydantic import BaseModel, ValidationError

class Patient(BaseModel):
    name: str
    age: int
```

```python
try:
    patient = Patient(
        name="Rahul",
        age="abc"
    )
except ValidationError as e:
    print(e)
```

The error contains information about what went wrong.

### Remember

```text
Wrong input
    ↓
Pydantic validation
    ↓
ValidationError
```

---

# 13. Dictionary → Pydantic Object

Pydantic models can be created from dictionary-like data.

```python
data = {
    "name": "Rahul",
    "age": 20
}

patient = Patient(**data)
```

Now:

```python
patient.name
patient.age
```

can be used.

In Pydantic v2, another important approach is:

```python
patient = Patient.model_validate(data)
```

### Difference

```python
Patient(**data)
```

uses normal Python argument unpacking.

```python
Patient.model_validate(data)
```

explicitly tells Pydantic:

> Validate this object as a `Patient` model.

---

# 14. Pydantic Object → Dictionary

A Pydantic model can be converted back into a dictionary.

In Pydantic v2:

```python
patient.model_dump()
```

Example:

```python
patient = Patient(
    name="Rahul",
    age=20
)

data = patient.model_dump()

print(data)
```

Result:

```python
{
    "name": "Rahul",
    "age": 20
}
```

---

# 15. Pydantic Object → JSON

In Pydantic v2:

```python
patient.model_dump_json()
```

This produces a JSON representation.

Example:

```python
json_data = patient.model_dump_json()

print(json_data)
```

---

# 16. Nested Pydantic Models

Pydantic models can contain other Pydantic models.

```python
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    country: str

class Patient(BaseModel):
    name: str
    age: int
    address: Address
```

Now:

```python
patient = Patient(
    name="Rahul",
    age=20,
    address={
        "city": "Delhi",
        "country": "India"
    }
)
```

Pydantic can validate the nested `address` structure as well.

Think of it as:

```text
Patient
│
├── name
├── age
│
└── address
      ├── city
      └── country
```

---

# 17. Pydantic with FastAPI

Pydantic is deeply integrated with FastAPI.

A Pydantic model can be used to define the structure of a request body.

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

If the request doesn't satisfy the model, FastAPI automatically returns a validation error response.

---

# 18. Path / Query Parameters vs Request Body

This is important when learning FastAPI.

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

### Request Body using Pydantic

```python
@app.post("/patient")
def create_patient(patient: Patient):
    ...
```

Example JSON:

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

# 19. Pydantic vs Normal Python Class

### Normal Python Class

```python
class Patient:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

Python itself does not automatically enforce:

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

Pydantic adds structured validation and parsing.

---

# 20. Pydantic vs Dictionary

A dictionary is flexible:

```python
patient = {
    "name": "Rahul",
    "age": 20
}
```

But a dictionary does not itself define a strict schema.

A Pydantic model defines:

```python
class Patient(BaseModel):
    name: str
    age: int
```

So:

```text
Dictionary
→ Raw / flexible data

Pydantic Model
→ Structured + validated data
```

---

# 21. Important Pydantic Methods — Pydantic v2

| Method | Purpose |
|---|---|
| `model_validate()` | Validate input and create a model |
| `model_dump()` | Convert model to dictionary |
| `model_dump_json()` | Convert model to JSON |
| `model_validate_json()` | Validate JSON input |

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

> **Revision Note:** You may find older tutorials using methods such as `.dict()` and `.json()`. Pydantic v2 uses `model_dump()` and `model_dump_json()` as the preferred methods.

---

# 22. Complete Example

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Patient(BaseModel):
    name: str
    age: int = Field(gt=0)
    weight: float = Field(gt=0)
    height: float = Field(gt=0)


@app.post("/patient")
def create_patient(patient: Patient):

    return {
        "message": "Patient created successfully",
        "patient": patient.model_dump()
    }
```

Request:

```json
{
    "name": "Rahul",
    "age": 20,
    "weight": 65.5,
    "height": 175
}
```

Flow:

```text
JSON Request
     ↓
FastAPI
     ↓
Pydantic Patient Model
     ↓
Validate fields
     ↓
Check constraints
     ↓
Create Patient object
     ↓
Function receives validated object
     ↓
model_dump()
     ↓
Dictionary / JSON response
```

---

# 23. Key Terms to Remember

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

Checking whether input satisfies the defined rules.

### Parsing / Coercion

Converting compatible input into the expected representation when Pydantic's rules allow it.

### Pydantic Model

A Python class derived from `BaseModel` that defines and validates a data schema.

### Pydantic Object

An instance created from a Pydantic model.

### ValidationError

The error raised when input fails Pydantic validation.

---

# 24. Quick Revision

```text
                    PYDANTIC
                       │
                       ↓
                Define a Schema
                       │
                       ↓
                 BaseModel
                       │
                       ↓
              Define Fields + Types
                       │
                       ↓
              Add Constraints
                  (Field)
                       │
                       ↓
                Raw Input Data
                       │
                       ↓
            Validation + Parsing
                 /          \
              Valid        Invalid
                ↓             ↓
        Pydantic Object   ValidationError
                ↓
          Use in Application
```

---

# 25. One-Line Revision Notes

```text
Pydantic
→ Data validation + parsing library.

BaseModel
→ Base class used to create Pydantic models.

Field()
→ Adds constraints/metadata to fields.

ValidationError
→ Raised when input fails validation.

model_validate()
→ Validates input and creates a model.

model_dump()
→ Converts model to dictionary.

model_dump_json()
→ Converts model to JSON.

FastAPI + Pydantic
→ FastAPI uses Pydantic models extensively for request
  validation and structured data handling.
```

---

# 26. Most Important Mental Model

If you remember only one thing, remember this:

```text
                    RAW DATA
                       │
                       ↓
              ┌─────────────────┐
              │ Pydantic Model  │
              │                 │
              │ Schema          │
              │ Types           │
              │ Constraints     │
              └────────┬────────┘
                       ↓
                  VALIDATION
                       │
              ┌────────┴────────┐
              ↓                 ↓
           VALID             INVALID
              ↓                 ↓
      Pydantic Object     ValidationError
              ↓
       Use in Application
```

> **Core idea:** Pydantic lets you define what your data **should look like**, validates incoming data against that definition, and gives you a structured Python object to work with.