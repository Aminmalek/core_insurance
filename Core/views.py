import uuid
from django.http import HttpResponse
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from Health_Insurance.settings import BASE_DIR
from authenticate.models import User
from .decorators import is_company
from .models import Message
from .serializers import MessageSerializer


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


class MessageView(APIView):

    @is_company
    def post(self, request):
        user = request.user
        data = request.data
        receiver = data['receiver']
        message = data['message']
        if data:
            receiver = User.objects.get(username=receiver)
            Message.objects.create(
                sender=user, message=message, receiver=receiver)
            return Response({"message": "message created successfuly"})
        else:
            return Response({"error": "please send your message first"}, status=status.HTTP_400_BAD_REQUEST)

    @is_company
    def get(self, request):
        user = request.user
        sender = request.query_params.get('sender', None)
        if sender is not None:
            message = Message.objects.filter(sender=sender)
            serializer = MessageSerializer(message, many=True)
            return Response({"message": serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            message = Message.objects.filter(receiver=user.id)
            serializer = MessageSerializer(message, many=True)
            return Response({"message": serializer.data})

    @is_company
    def put(self, request, id):
        user = request.user
        data = request.data
        response = data['response']
        message = Message.objects.get(id=id)
        if message.receiver == user:
            message.response = response
            message.save()
            return Response({"message": "message updated successfuly"})
        else:
            return Response({"error": "you can only update your messages"}, status=status.HTTP_400_BAD_REQUEST)

    @is_company
    def delete(self, request, id):
        user = request.user
        message = Message.objects.get(id=id)
        if message.sender == user:
            message.delete()
            return Response({"message": "message deleted successfuly"})
        else:
            return Response({"error": "you can only delete your messages"}, status=status.HTTP_400_BAD_REQUEST)
