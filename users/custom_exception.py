# from django.core.exceptions import ValidationError
# from django.http import Http404
# from rest_framework import status
# from rest_framework.exceptions import MethodNotAllowed
# from rest_framework.response import Response
# from rest_framework.views import exception_handler

# from . import models

# def message_correction(message):
#     errors = str(message).replace("[", "").replace("]", "").replace("'", "")
#     return errors

# def custom_exception_handler(exc, context):
#     response = None

#     if isinstance(exc, MethodNotAllowed):
#         response = Response(
#             {"error": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
#         )
#     elif isinstance(exc, Http404):
#         errors = (
#             getattr(exc, "message", None) or getattr(exc, "messages", None) or str(exc)
#         )
#         errors = message_correction(errors)
#         response = Response({"error": errors}, status=status.HTTP_404_NOT_FOUND)
#     elif isinstance(exc, models.CustomUser.DoesNotExist):
#         errors = (
#             getattr(exc, "message", None) or getattr(exc, "messages", None) or str(exc)
#         )
#         errors = message_correction(errors)
#         response = Response(
#             {"error": errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
#     elif isinstance(exc, Exception):
#         errors = (
#             getattr(exc, "message", None) or getattr(exc, "messages", None) or str(exc)
#         )
#         errors = message_correction(errors)
#         response = Response(
#             {"error": errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
#     if response is None:
#         response = exception_handler(exc, context)

#     return response