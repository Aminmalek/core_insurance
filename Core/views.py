from os import error
import uuid
from django.http import HttpResponse
from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from Health_Insurance.settings import BASE_DIR
from rest_framework.decorators import action
from authenticate.models import User
from authenticate.serializers import UserSerializer
from .decorators import type_check, type_confirmation
from .models import Message
from .serializers import MessageSerializer
from rest_framework.exceptions import NotFound

class FileView(APIView):
    parser_class = (FileUploadParser,)
    permission_classes = (permissions.AllowAny,)

    def save_uploaded_file(self, file, file_name):
        # must save format in saving media
        uuid_file_name = str(uuid.uuid4())
        with open(BASE_DIR / 'media' / uuid_file_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
        return uuid_file_name

    def put(self, request):
        file_obj = request.FILES['file']
        file_name = self.save_uploaded_file(file_obj, file_obj.name)
        return Response({"name": file_name})

    def get(self, request):
        file_name = request.query_params.get('file_name', None)
        with open(BASE_DIR / 'media' / file_name, 'rb') as file:
            # This part is for download the file in clients browser
            response = HttpResponse(
                file, content_type='application/force-download')
            response['Content-Disposition'] = f'inline; filename="{file_name}"'
        return response


class MessageViewSet(viewsets.ViewSet):

    @type_check(("Company", "Vendor", "CompanyAdmin"))
    def create(self, request):
        user = request.user
        data = request.data
        if data:
            receiver = data['receiver']
            message = data['message']
            receiver = User.objects.get(username=receiver)
            Message.objects.create(
                sender=user, message=message, receiver=receiver)
            return Response({"message": "message created successfuly"})
        else:
            return Response({"error": "please send your message first"}, status=status.HTTP_400_BAD_REQUEST)

    @type_check(("Company", "Vendor", "CompanyAdmin"))
    @action(['GET'], detail=False, url_path='sent-messages', url_name='sent-messages',)
    def list_sent_messages(self, request):
        user = request.user
        message = Message.objects.filter(sender=user)
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)

    @type_check(("Company", "Vendor", "CompanyAdmin"))
    @action(['GET'], detail=False, url_path='received-messages', url_name='received-messages',)
    def list_received_messages(self, request):
        user = request.user
        message = Message.objects.filter(receiver=user.id)
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)

    @type_check(("Company", "Vendor", "CompanyAdmin"))
    def update(self, request, pk):
        user = request.user
        data = request.data
        response = data['response']
        message = Message.objects.get(id=pk)
        if message.receiver == user:
            message.response = response
            message.save()
            return Response({"message": "message updated successfuly"})
        else:
            return Response({"error": "you can only send response to your messages"}, status=status.HTTP_400_BAD_REQUEST)

    @type_check(("Company", "Vendor", "CompanyAdmin"))
    @action(['GET'], detail=False, url_path='get-users', url_name='get-users',)
    def get_users(self, request):
        users = User.objects.filter(type__in=[1, 2, 6])
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @type_check(("Company", "Vendor", "CompanyAdmin"))
    def delete(self, request, pk):
        user = request.user
        try:
            message = Message.objects.get(id=pk)
        except Message.DoesNotExist:
            raise NotFound(detail="message doesn't exist", code=404)
        if message.sender == user:
            message.delete()
            return Response({"message": "message deleted successfuly"})
        else:
            return Response({"error": "you can only delete your messages"}, status=status.HTTP_400_BAD_REQUEST)

    """ data={k: v for k, v in dict(request.data).items() if v}
       
        d = ExitAndEnterTime.objects.filter(id=id).update(**data)"""
