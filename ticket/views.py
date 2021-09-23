from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . models import Ticket
from . serializers import TicketSerializer


class TicketView(APIView):

    def post(self, request):
        """
            For add new ticket by holder or insured
        """
        data = request.data
        user = request.user
        if user.type == 'Insured' or user.type == 'Holder':
            ticket_name = data['name']
            description = data['description']
            Ticket.objects.create(
                user=user, name=ticket_name, description=description)
            content = {"message": "Ticket created successfuly"}
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            content = {"message": "you are not authenticated to do this"}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        """
            For view all tickets of insured or holder by user id
        """
        user = request.user
        if user.type == 'Holder' or user.type == 'Insured':
            try:
                # I used filter because user can have many tickits
                tickets_of_user = Ticket.objects.filter(user=user.id)
            except:
                content = {"message": "There is not any ticket for this user"}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            serializer = TicketSerializer(tickets_of_user, many=True)
            return Response(serializer.data)
        else:
            content = {"message": "you are not permited to do this action"}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)


# This methods can user here or in vendor app we can chanage it
'''
   

    def put(self,request):

        data = request.data
        # I add [6:] because Token set to header like this Token e6r5g4e6r54ge
        token = Token.objects.get(
            key=request.META.get('HTTP_AUTHORIZATION')[6:])
        user = User.objects.get(auth_token=token)
        if user.type == 'Vendor':
            ticket_status = bool(data['status'])
            ticket_id = data['ticket_id']
            ticket_for_update = Ticket.objects.get(id=ticket_id)
            return Response({ticket_for_update.name})
        else:
            content = {"message": "you are not permited to do this action"}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
'''
