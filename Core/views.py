from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from Health_Insurance.settings import BASE_DIR


class FileView(APIView):
    parser_class = (FileUploadParser,)
    
    def save_uploaded_file(self,file,file_name):
        import uuid
        id = str(uuid.uuid4())
        with open(BASE_DIR / 'media'/id, 'wb+') as destination:
       
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
        return id

    def put(self,request):

        file_obj = request.FILES['file']
        id = self.save_uploaded_file(file_obj,file_obj.name)

        return Response({"name":id})
