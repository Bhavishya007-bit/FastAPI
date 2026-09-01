# PUT and DELETE HTTP Methods in FastAPI

This project demonstrates how to implement **Update (PUT)** and **Delete (DELETE)** operations in FastAPI using a patient dataset stored in a JSON file.

## Endpoints

- `PUT /edit/{patient_id}` → Update an existing patient's information
- `DELETE /delete/{patient_id}` → Delete an existing patient

---

## PUT Method — Updating Patient Data

A `PUT` request is used to update an existing resource.

```python
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient does not exist')

    existing_patient_info = data[patient_id]

    update_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in update_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id

    patient_pydantic_obj = Patient(**existing_patient_info)

    existing_patient_info = patient_pydantic_obj.model_dump(exclude={'id'})

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(
        status_code=200,
        content={'message': 'patient updated'}
    )
```

### How It Works

### 1. Load Existing Data

```python
data = load_data()
```

This reads the patient data from the JSON file and stores it in a Python dictionary.

---

### 2. Check Whether the Patient Exists

```python
if patient_id not in data:
    raise HTTPException(
        status_code=404,
        detail='Patient does not exist'
    )
```

Before updating a patient, we first check whether the given `patient_id` exists.

If the patient does not exist, the API returns:

```text
404 Not Found
```

---

### 3. Get Existing Patient Information

```python
existing_patient_info = data[patient_id]
```

This retrieves the current information of the patient.

For example:

```python
{
    "name": "John",
    "age": 25,
    "height": 1.75,
    "weight": 70
}
```

---

### 4. Extract Only the Fields Provided by the User

```python
update_patient_info = patient_update.model_dump(
    exclude_unset=True
)
```

`model_dump()` converts a Pydantic object into a Python dictionary.

The important argument is:

```python
exclude_unset=True
```

This means:

> Include only those fields that were explicitly provided by the user.

For example, if the request body is:

```json
{
    "weight": 75
}
```

then:

```python
patient_update.model_dump(exclude_unset=True)
```

returns:

```python
{
    "weight": 75
}
```

This prevents other optional fields from being unnecessarily overwritten.

---

### 5. Update Existing Values

```python
for key, value in update_patient_info.items():
    existing_patient_info[key] = value
```

Suppose:

```python
update_patient_info = {
    "weight": 75,
    "age": 26
}
```

Then the loop updates only these values.

Before:

```python
{
    "name": "John",
    "age": 25,
    "height": 1.75,
    "weight": 70
}
```

After:

```python
{
    "name": "John",
    "age": 26,
    "height": 1.75,
    "weight": 75
}
```

---

### 6. Add the Patient ID Temporarily

```python
existing_patient_info['id'] = patient_id
```

In the JSON file, the patient ID may be stored as the dictionary key:

```python
{
    "P001": {
        "name": "John",
        "age": 25
    }
}
```

But the `Patient` Pydantic model may require an `id` field.

Therefore, we temporarily add it before validation.

---

### 7. Validate the Updated Patient

```python
patient_pydantic_obj = Patient(**existing_patient_info)
```

This creates a `Patient` Pydantic object using the updated data.

Pydantic validates the complete patient information according to the rules defined in the `Patient` model.

---

### 8. Convert Back to a Dictionary

```python
existing_patient_info = patient_pydantic_obj.model_dump(
    exclude={'id'}
)
```

The validated Pydantic object is converted back into a Python dictionary.

The `id` field is excluded because it is already being used as the key in the main data dictionary.

---

### 9. Store the Updated Patient

```python
data[patient_id] = existing_patient_info
```

The updated information is assigned back to the patient ID.

---

### 10. Save the Data

```python
save_data(data)
```

The updated dictionary is written back to the JSON file.

---

### 11. Return the Response

```python
return JSONResponse(
    status_code=200,
    content={'message': 'patient updated'}
)
```

Successful response:

```json
{
    "message": "patient updated"
}
```

---

## PUT Request Flow

```text
Client
  |
  | PUT /edit/P001
  |
  | Request Body
  | {"weight": 75}
  |
  v
Load Data
  |
  v
Check Patient ID
  |
  +---- Not Found ----> 404
  |
  v
Get Existing Patient
  |
  v
Extract Provided Fields
  |
  v
Update Values
  |
  v
Validate with Pydantic
  |
  v
Save Updated Data
  |
  v
200 OK
```

---

## DELETE Method — Removing a Patient

A `DELETE` request is used to remove an existing resource.

```python
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]

    save_data(data)

    return JSONResponse(
        status_code=200,
        content={'message': 'patient deleted'}
    )
```

---

## How DELETE Works

### 1. Load Existing Data

```python
data = load_data()
```

The patient data is loaded from the JSON file.

---

### 2. Check Whether the Patient Exists

```python
if patient_id not in data:
    raise HTTPException(
        status_code=404,
        detail='Patient not found'
    )
```

If the patient does not exist, the API returns:

```text
404 Not Found
```

---

### 3. Delete the Patient

```python
del data[patient_id]
```

Python's `del` statement removes the patient entry from the dictionary.

For example:

Before:

```python
{
    "P001": {
        "name": "John"
    },
    "P002": {
        "name": "Alice"
    }
}
```

After:

```python
del data["P001"]
```

Result:

```python
{
    "P002": {
        "name": "Alice"
    }
}
```

---

### 4. Save the Modified Data

```python
save_data(data)
```

After deleting the patient from the Python dictionary, the modified data must be written back to the JSON file.

Otherwise, the deletion would not persist.

---

### 5. Return the Response

```python
return JSONResponse(
    status_code=200,
    content={'message': 'patient deleted'}
)
```

Successful response:

```json
{
    "message": "patient deleted"
}
```

---

## DELETE Request Flow

```text
Client
  |
  | DELETE /delete/P001
  |
  v
Load Data
  |
  v
Check Patient ID
  |
  +---- Not Found ----> 404
  |
  v
Delete Patient
  |
  v
Save Data
  |
  v
200 OK
```

---

## PUT vs DELETE

| Feature | PUT | DELETE |
|---|---|---|
| Purpose | Update a resource | Remove a resource |
| Endpoint | `/edit/{patient_id}` | `/delete/{patient_id}` |
| Path Parameter | Yes | Yes |
| Request Body | Yes | Usually No |
| Checks Patient | Yes | Yes |
| Updates Dictionary | Yes | No |
| Deletes Dictionary Entry | No | Yes |
| Saves Data | Yes | Yes |
| Success Status | `200` | `200` |
| Not Found Status | `404` | `404` |

---

## Important Concepts

### Path Parameter

```python
@app.put('/edit/{patient_id}')
```

Here:

```text
{patient_id}
```

is a path parameter.

Example:

```text
/edit/P001
```

FastAPI extracts:

```python
patient_id = "P001"
```

---

### Request Body

```python
patient_update: PatientUpdate
```

FastAPI reads the request body and validates it using the `PatientUpdate` Pydantic model.

Example request body:

```json
{
    "weight": 75
}
```

---

### `model_dump()`

```python
patient_update.model_dump()
```

Converts a Pydantic model into a Python dictionary.

---

### `exclude_unset=True`

```python
patient_update.model_dump(exclude_unset=True)
```

Returns only the fields explicitly provided by the client.

This is very useful when performing partial updates.

---

### `HTTPException`

```python
raise HTTPException(
    status_code=404,
    detail='Patient not found'
)
```

Used to return an HTTP error response from a FastAPI endpoint.

---

### `JSONResponse`

```python
return JSONResponse(
    status_code=200,
    content={'message': 'patient updated'}
)
```

Used to manually return JSON content with a specific HTTP status code.

---

## PUT vs PATCH

This endpoint uses:

```python
model_dump(exclude_unset=True)
```

which means only the fields provided by the client are changed.

This behavior is technically similar to a **partial update**.

In REST APIs:

- `PUT` is generally used to replace or update a complete resource.
- `PATCH` is generally used for partial updates.

So the current endpoint behaves more like a `PATCH` operation even though `PUT` is being used.

This is acceptable for learning purposes, but it is useful to understand the distinction.

---

## CRUD and HTTP Methods

| CRUD Operation | HTTP Method |
|---|---|
| Create | `POST` |
| Read | `GET` |
| Update | `PUT` / `PATCH` |
| Delete | `DELETE` |

```text
CREATE  -> POST
READ    -> GET
UPDATE  -> PUT / PATCH
DELETE  -> DELETE
```

---

## Quick Revision

### Update

```text
Load Data
   |
Check Patient
   |
Get Existing Data
   |
Get Fields Sent by Client
   |
Update Fields
   |
Validate with Pydantic
   |
Save
```

Important code:

```python
updates = patient_update.model_dump(exclude_unset=True)

for key, value in updates.items():
    existing_patient_info[key] = value
```

---

### Delete

```text
Load Data
   |
Check Patient
   |
Delete Patient
   |
Save
```

Important code:

```python
del data[patient_id]
```

---

## Key Takeaways

1. `PUT` is used to update an existing resource.
2. `DELETE` is used to remove a resource.
3. `{patient_id}` is a path parameter.
4. `PatientUpdate` validates the request body.
5. `model_dump()` converts a Pydantic model into a dictionary.
6. `exclude_unset=True` returns only explicitly provided fields.
7. Always check whether the patient exists before updating or deleting.
8. Use `HTTPException(status_code=404)` for missing resources.
9. Validate updated data using the complete `Patient` Pydantic model.
10. Always call `save_data()` after changing the dictionary.
