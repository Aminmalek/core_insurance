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

    def create_insurances(self):
        Insurance.objects.create(id=223,
            name="2بیمه خسارات درمانی", description="پرداخت هزینه های درمانی شامل هزینه های دارویی و بیمارستانی", price=10000000,
            register_form={"وضعیت تاهل": "مجرد",
                           "حقوق": 684,
                           "تعداد فرزندان": "0",
                           "بیماری خاص": "آری",
                           "نام بیماری": "ایدز"},
            claim_form={"مکان وقوع": "تهران",
                        "شهر محل زندگی": "Tehran",
                        "میزان": 8456,
                        "زمان": "1400/02/05"})

        Insurance.objects.create(
            name="2بیمه شخص ثالث", description="پرداخت هزینه های مربوط به تصادفات و خسارات ناشی از سوانح", price=10000000,
            register_form={"وضعیت تاهل": "مجرد",
                           "حقوق": 684,
                           "تعداد فرزندان": "0",
                           "زمان حادثه":"صبح",
                           "نام بیماری": "ایدز"}, 
                           claim_form={"مکان وقوع": "تهران",
                                        "شهر محل زندگی": "Tehran",
                                        "میزان": 8456,
                                        "زمان": "1400/02/05"})
        self.stdout.write("insurances created")
    def handle(self, *args, **kwargs):
        self.create_insurances()
        self.stdout.write("insurances created")