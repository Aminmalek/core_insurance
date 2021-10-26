from rest_framework.response import Response
from rest_framework import status
from functools import wraps

def is_insured(view):
    @wraps(view)
    def wrapper_func(self, request, *args, **Kwargs):
        if request.user.type == "Insured":
            # change your logic here
            return view(self, request, *args, **Kwargs)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    return wrapper_func


def is_company(view):
    def wrapper_func(self, request, *args, **Kwargs):
        if request.user.type == "Company":
            # change your logic here
            return view(self, request, *args, **Kwargs)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    return wrapper_func


def is_company_or_insured(view):
    def wrapper_func(self, request, *args, **Kwargs):
        if request.user.type == "Company" or request.user.type == "Insured":
            # change your logic here
            return view(self, request, *args, **Kwargs)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    return wrapper_func


def is_vendor(view):
    def wrapper_func(self, request, *args, **Kwargs):
        if request.user.type == "Vendor":
            # change your logic here
            return view(self, request, *args, **Kwargs)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    return wrapper_func


def is_holder(view):
    def wrapper_func(self, request, *args, **Kwargs):
        if request.user.type == "Holder":
            # change your logic here
            return view(self, request, *args, **Kwargs)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    return wrapper_func


def is_super_holder(view):
    def wrapper_func(self, request, *args, **Kwargs):
        if request.user.type == "SuperHolder":
            # change your logic here
            return view(self, request, *args, **Kwargs)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    return wrapper_func

def is_holder_superholder_insured(view):
    def wrapper_func(self, request, *args, **Kwargs):
        if request.user.type == "Insured" or  request.user.type == "Holder" or request.user.type == "SuperHolder":
            # change your logic here
            return view(self, request, *args, **Kwargs)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    return wrapper_func

def is_holder_insured(view):
    def wrapper_func(self, request, *args, **Kwargs):
        if request.user.type == "Holder" or request.user.type == "Insured":
            # change your logic here
            return view(self, request, *args, **Kwargs)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    return wrapper_func

def role_needed(*permissions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            nonlocal permissions  # Just to make sure `permission` is available in this scope
            # Implement here how to deal with permissions
            return f(*args, **kwargs)
        return decorated_function
    return decorator
"""
class TestView(APIView):
    
    @is_insured
    @is_active
    def get(self,request):
        
        return Response({"hello"})
"""
