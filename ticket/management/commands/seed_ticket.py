from django.core.management.base import BaseCommand
from authenticate.models import User
from insurance.models import Insurance
from ticket.models import Ticket, Claim
from payment.models import InsuranceConnector


class Command(BaseCommand):
    """
    creates some database objects to for development and testing
    """

    def create_tickets(self):
        user = User.objects.get(username=1234567892)
        Ticket.objects.create(user=user, name="مشکل در بیمه نامه",
                              description="یک مشتری بعد از خرید بیمه نامه فورا دچار مشکل شده",)
        user2 = User.objects.get(username=1234567893)
        Ticket.objects.create(user=user2, name="عدم ثبت تخفیف هنگام خرید بیمه نامه",
                              description="عدم ثبت بیمه نامه بعد از خرید لطفا سریعا پیگیری شود",)
        user3 = User.objects.get(username=1234567895)
        Ticket.objects.create(user=user2, name="چگونه بیمه جدید بخرم",
                              description="برای خرید بیمه جدید ارور میگیرم لطفا راهنمایی کنید",)
        self.stdout.write("tickets created")

    def create_claims(self):
        user = User.objects.get(username=1234567895)
        insurance = Insurance.objects.get(id=10)
        ins = InsuranceConnector.objects.create(user=user,insurance=insurance,)
        Claim.objects.create(user=user, insurance=ins, 
        title="جراحی قلب باز", 
        description="من جراحی قلب باز انجام داده ام", 
        status="Opened", 
        
        claim_form={"مکان وقوع": "تهران",
                        "شهر محل زندگی": "Tehran",
                        "میزان": 55000,
                        "زمان": "1400/02/05"})
        Claim.objects.create(user=user, insurance=ins, 
        title="هزینه داروی خاص", 
        description="داروی خاص خریداری شده برای بیماری", 
        status="Opened", 
       
        claim_form={"مکان وقوع": "تهران",
                        "شهر محل زندگی": "Tehran",
                        "میزان": 25000,
                        "زمان": "1400/02/20"})
        self.stdout.write("claims created")
    def handle(self, *args, **kwargs):

        self.create_tickets()
        self.create_claims()