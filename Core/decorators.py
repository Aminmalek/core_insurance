from rest_framework.response import Response
from rest_framework import status
from functools import wraps


def role_needed(*permissions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            nonlocal permissions  # Just to make sure `permission` is available in this scope

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def type_check(*permissions):
    def decorator(view):
        @wraps(view)
        def decorated_function(self, request, *args, **kwargs):
            permissions_dic = {"Company": 1, "Vendor": 2,
                               "SuperHolder": 3, "Holder": 4, "Insured": 5,"CompanyAdmin": 6}
            permission_num = []

            for per in permissions[0]:
                permission_num.append(permissions_dic[per])

            if request.user.type not in permission_num:
                return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return view(self, request, *args, **kwargs)
        return decorated_function
    return decorator
