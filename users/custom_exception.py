from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import exception_handler

from . import models

def message_correction(message):
    # Removes square brackets and single quotes from error messages
    errors = str(message).replace("[", "").replace("]", "").replace("'", "")
    return errors

def custom_exception_handler(exc, context):
    response = None # Initialize the response variable
    
    # Custom handler to provide consistent error responses.
    # Depending on the type of exception, returns a Response with appropriate status code and message.
    
    # Handle "Method Not Allowed" exceptions
    if isinstance(exc, MethodNotAllowed):
        response = Response(
            {"error": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
        
    # Handle "Does Not Exist" exceptions for the CustomUser model
    elif isinstance(exc, models.CustomUser.DoesNotExist):
        # Extract the error message from the exception
        errors = (
            getattr(exc, "message", None)  # Check if the exception has a 'message' attribute
            or getattr(exc, "messages", None)  # Check if the exception has 'messages' (list of errors)
            or str(exc)  # Default to string representation of the exception
        )
        # Clean up the error message using the helper function
        errors = message_correction(errors)
        response = Response(
            # Return the cleaned error message
            {"error": errors}, status=status.HTTP_400_BAD_REQUEST
        )
    
    # Handle all other exceptions
    else:
        errors = (
            getattr(exc, "message", None) or getattr(exc, "messages", None) or str(exc)
        )
        errors = message_correction(errors)
        response = Response(
            {"error": errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response