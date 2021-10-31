from django.core.management.base import BaseCommand
from authenticate.models import User
from insured.models import Insured
from super_holder.models import SuperHolder
from insurance.models import Insurance
from ticket.models import Ticket


class Command(BaseCommand):
    """
    creates some database objects to for development and testing
    """
    pass