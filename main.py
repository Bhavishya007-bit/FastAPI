# ============================================================
# FASTAPI - PATIENT DATA MANAGEMENT SYSTEM
# ============================================================
#
# THEORY:
# FastAPI is a modern Python web framework used to build APIs.
#
# An API (Application Programming Interface) allows different
# applications to communicate with each other.
#
# FastAPI provides:
# - Routing
# - Automatic validation
# - Automatic API documentation (Swagger UI)
# - Type hints based request validation
# - HTTPException for handling HTTP errors
#
# Common HTTP methods:
# GET     -> Retrieve data
# POST    -> Create data
# PUT     -> Update/replace data
# DELETE  -> Delete data
# ============================================================


from fastapi import FastAPI, Path, HTTPException, Query
import json


# ============================================================
# 1. LOADING DATA FROM JSON FILE
# ============================================================

def load_data():
    """
    Loads patient data from patient.json.

    THEORY:
    json.load() reads a JSON file and converts it into
    a Python object.

    If the JSON contains an object like:

        {
            "P001": {...},
            "P002": {...}
        }

    then json.load() converts it into a Python dictionary.

    So the returned 'data' is a dictionary.
    """

    # 'with open()' automatically closes the file after use.
    with open('patient.json', 'r') as f:
        data = json.load(f)

    return data


# ============================================================
# 2. CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI()

# THEORY:
# FastAPI() creates the main FastAPI application object.
#
# 'app' is then used to create routes/endpoints.
#
# Example:
#
#     @app.get("/")
#
# means:
# "When a client sends a GET request to '/', execute
# the function below it."
# ============================================================


# ============================================================
# 3. ROOT ROUTE
# ============================================================

@app.get("/")
# @app.get() is a DECORATOR.
#
# It tells FastAPI:
# "Map this URL path to the function below."
#
# Here:
# GET /  ->  hello()

def hello():
    return {'message': 'Patient data management system'}


# ============================================================
# 4. ABOUT ROUTE
# ============================================================

@app.get("/about")
def about():
    return {
        'message': 'Hi this is my first FastAPI code thank you hehehe'
    }


# ============================================================
# 5. VIEW ALL PATIENTS
# ============================================================

@app.get("/view")
def view():

    # Load patient data from patient.json
    data = load_data()

    # Return the complete dictionary as the API response.
    #
    # FastAPI automatically converts Python dictionaries
    # into JSON responses.
    return data


# ============================================================
# 6. PATH PARAMETER
# ============================================================

@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,
        description="ID of the patient in DB",
        example="P001"
    )
):
    """
    Fetch a specific patient using patient_id.

    THEORY:
    A PATH PARAMETER is a variable part of the URL.

    Example:

        /patient/P001

    Here:

        patient_id = P001

    Path parameters are generally used when we want to
    identify a specific resource.

    Example:

        /patient/P001
        /patient/P002
        /patient/P003

    Each URL refers to a particular patient.
    """

    data = load_data()

    # Check whether the requested patient_id exists
    # as a key in the dictionary.
    if patient_id in data:

        # Return only the requested patient's information.
        return data[patient_id]

    # --------------------------------------------------------
    # HTTPException
    # --------------------------------------------------------
    #
    # If the patient doesn't exist, we should NOT simply return:
    #
    #     {'error': 'patient not found'}
    #
    # because FastAPI would normally return HTTP status code 200.
    #
    # 200 means:
    # "The request was successful."
    #
    # Instead, we raise an HTTPException with status code 404.
    #
    # 404 = Resource Not Found
    #
    # HTTPException is provided by FastAPI and is used to
    # return proper HTTP error responses.
    # --------------------------------------------------------

    raise HTTPException(
        status_code=404,
        detail='Patient not found'
    )


# ============================================================
# 7. QUERY PARAMETERS + SORTING
# ============================================================

@app.get('/sort')
def sort_patient(
    sort_by: str = Query(
        ...,
        description='Sort on the basis of height, weight, or bmi'
    ),
    order: str = Query(
        'asc',
        description='Sort in asc or desc order'
    )
):
    """
    Sort patient data according to height, weight, or BMI.

    THEORY:
    QUERY PARAMETERS are optional key-value pairs added
    to the end of a URL.

    Example:

        /sort?sort_by=height&order=asc

    Here:

        sort_by=height
        order=asc

    The '?' marks the beginning of query parameters.

    '&' separates multiple query parameters.

    Query parameters are commonly used for:

    - Filtering
    - Searching
    - Sorting
    - Pagination

    --------------------------------------------------------

    PATH PARAMETER vs QUERY PARAMETER

    Path parameter:

        /patient/P001

    Used to identify a specific resource.

    Query parameter:

        /sort?sort_by=height

    Used to control HOW we want the data to be returned.
    """


    # ========================================================
    # 8. VALIDATING sort_by
    # ========================================================

    # These are the only fields that the user is allowed
    # to use for sorting.
    valid_fields = ['height', 'weight', 'bmi']

    # Check whether the requested sorting field is valid.
    if sort_by not in valid_fields:

        # 400 = Bad Request
        #
        # It means the client sent an invalid request.
        raise HTTPException(
            status_code=400,
            detail=f'Invalid field select from {valid_fields}'
        )


    # ========================================================
    # 9. VALIDATING order
    # ========================================================

    # Only 'asc' and 'desc' are accepted.
    if order not in ['asc', 'desc']:

        raise HTTPException(
            status_code=400,
            detail='Invalid order select between asc or desc'
        )


    # ========================================================
    # 10. LOAD PATIENT DATA
    # ========================================================

    data = load_data()


    # ========================================================
    # 11. CONVERT asc/desc INTO True/False
    # ========================================================

    # Python's sorted() function uses:
    #
    #     reverse=False  -> ascending order
    #     reverse=True   -> descending order
    #
    # Therefore:
    #
    #     order == 'desc' -> True
    #     order == 'asc'  -> False

    sort_order = True if order == 'desc' else False


    # ========================================================
    # 12. SORT THE PATIENT DATA
    # ========================================================

    sorted_data = sorted(
        data.values(),

        # THEORY:
        # data.values() gives us the actual patient records.
        #
        # Example dictionary:
        #
        # {
        #     "P001": {"height": 175, ...},
        #     "P002": {"height": 165, ...}
        # }
        #
        # data.values() gives:
        #
        # {"height": 175, ...}
        # {"height": 165, ...}
        #
        # We want these patient records because we want
        # to sort them based on height/weight/BMI.

        key=lambda x: x.get(sort_by, 0),

        # THEORY:
        # key tells sorted() WHICH VALUE should be used
        # for sorting.
        #
        # If:
        #
        #     sort_by = "height"
        #
        # then:
        #
        #     x.get(sort_by, 0)
        #
        # becomes:
        #
        #     x.get("height", 0)
        #
        # So sorted() sorts patients according to height.
        #
        # .get(key, default) is used instead of x[key]
        # because if the key doesn't exist, it returns 0
        # instead of raising a KeyError.

        reverse=sort_order

        # reverse=False -> ascending
        # reverse=True  -> descending
    )


    # Return the sorted patient records.
    return sorted_data