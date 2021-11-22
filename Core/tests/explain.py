from django.contrib import auth
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from authenticate.models import User


class UserTestView(APIView):
    def get(self, request):
        a = (User.objects.filter(username="475274524752").explain(), (User.objects.filter(phone="912").explain()))

        user=User.objects.create_user(username="4545452", password="654654", first_name="amin",
                                        last_name="malek", phone=9421518515, type=5, bank_account_number=878454876546546574654)
        token=Token.objects.create(user=user)

        token, created=Token.objects.get_or_create(user=user)

        users=User.objects.filter(type=5)

        users=User.objects.all()

        user=User.objects.get(id=2)
        return Response({"message": "successfull test of user done"})
