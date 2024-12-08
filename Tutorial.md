1. Read and Understand the README File

2. Install Python: Ensure Python is installed.
    Check with: python --version

3. Install Dependencies:
    a. pip install "fastapi[standard]"
    b. pip install SQLAlchemy


4. Implement the required Features
    a.Database ModelsDefine models for:

       i. User: Represents users on the platform.
       ii.VirtualPhoneNumber: Represents virtual phone numbers owned by users.
       iii.CallLog: Represents call logs for virtual phone numbers.

    b.API Endpoints
    Retrieve a list of virtual phone numbers owned by a user:
         GET /users/{user_id}/virtual-phone-numbers: Define a GET endpoint that takes a user_id as input and returns their phone numbers.
        example: http://127.0.0.1:8080/users/1/virtual-phone-numbers
    
    
    Create a new virtual phone number for a user:
       
        POST /users/{user_id}/virtual-phone-numbers:  Define a POST endpoint that accepts a user_id and number in the request body.
        example:Post http://127.0.0.1:8080/users/1/virtual-phone-numbers
        

5. Test Application
    a.Run the server
        fastapi dev .\main.
        uvicorn main:app --reload --port 8080
        
    b.Test Api endpoint with Postman or curl.
