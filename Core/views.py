from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from Health_Insurance.settings import BASE_DIR
from django.http import HttpResponse


class FileView(APIView):
    parser_class = (FileUploadParser,)
    
    def save_uploaded_file(self,file,file_name):
        
        import uuid
        uuid_file_name = str(uuid.uuid4())

        with open(BASE_DIR / 'media'/ uuid_file_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
        return uuid_file_name

    def put(self,request):
        file_obj = request.FILES['file']
        file_name = self.save_uploaded_file(file_obj,file_obj.name)
        return Response({"name":file_name})

    def get(self, request):
        file_name = request.query_params.get('file_name', None)
        with open(BASE_DIR / 'media' / file_name, 'rb') as file:
            # This part is for download the file in clients browser
            response = HttpResponse(file, content_type='application/force-download')
            response['Content-Disposition'] = f'inline; filename="{file_name}"'
        return response
          


