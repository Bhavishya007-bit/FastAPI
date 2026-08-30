# Query Parameters in FastAPI

## What are Query Parameters?

**Query parameters** are optional `key=value` pairs added at the **end of a URL**.

They are mainly used to pass additional information to the server without changing the actual API endpoint.

Common uses:

- Filtering data
- Sorting data
- Searching
- Pagination

---

## Basic Example

```text
/patients?city=Delhi&sort_by=age
```

Breakdown:

```text
/patients
    ↓
Endpoint / Path

?
↓
Start of query parameters

city=Delhi
↓
Filter patients by city

&

sort_by=age
↓
Sort patients by age
```

So this request basically means:

> **Give me patients from Delhi and sort them by age.**

---

## Important Symbols

### `?`

The `?` marks the **beginning of query parameters**.

```text
/patients?city=Delhi
```

---

### `key=value`

Every query parameter is generally written as:

```text
key=value
```

Example:

```text
city=Delhi
```

Here:

```text
city  → key
Delhi → value
```

---

### `&`

If we want to send **multiple query parameters**, they are separated using `&`.

```text
/patients?city=Delhi&sort_by=age
```

Here we have two query parameters:

```text
city=Delhi

sort_by=age
```

---

# Path Parameter vs Query Parameter

## Path Parameter

Used when the value identifies a **specific resource**.

```text
/patients/101
```

Meaning:

> Give me the patient whose ID is `101`.

---

## Query Parameter

Used when we want to **filter, sort, search, or modify how data is returned**.

```text
/patients?city=Delhi
```

Meaning:

> Give me patients whose city is Delhi.

---

## Easy Way to Remember

```text
/patients/101
          ↑
     Path Parameter
     "WHICH patient?"
```

```text
/patients?city=Delhi&sort_by=age
          ↑
     Query Parameters
     "HOW should I view/filter the patients?"
```

---

# FastAPI Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/patients")
def view_patients(city: str, sort_by: str):
    return {
        "city": city,
        "sort_by": sort_by
    }
```

Request:

```text
/patients?city=Delhi&sort_by=age
```

FastAPI automatically extracts:

```python
city = "Delhi"
sort_by = "age"
```

---

# Optional Query Parameters

Query parameters are often made optional.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/patients")
def view_patients(city: str | None = None):
    return {"city": city}
```

Now both requests are possible:

```text
/patients
```

and

```text
/patients?city=Delhi
```

Because the default value of `city` is:

```python
None
```

---

# Revision Summary

```text
Query Parameter
      ↓
Optional information added after URL
      ↓
Starts with ?
      ↓
Written as key=value
      ↓
Multiple parameters separated by &
      ↓
Used for:
Filtering
Sorting
Searching
Pagination
```

### Example

```text
/patients?city=Delhi&sort_by=age
```

```text
/patients      → endpoint
?              → starts query parameters
city=Delhi     → filtering
&              → separates parameters
sort_by=age    → sorting
```

> **Memory Trick:**  
> Path parameter = **Which resource?**  
> Query parameter = **How do I want the data?**