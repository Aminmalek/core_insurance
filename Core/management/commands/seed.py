from django.core.management.base import BaseCommand
from authenticate.models import User
from insured.models import Insured
from super_holder.models import SuperHolder
from insurance.models import Insurance
from ticket.models import Ticket
from payment.models import InsuranceConnector
from ticket.models import Claim


class Command(BaseCommand):
    """
    creates some database objects to for development and testing
    """

    def create_users(self):
        try:
            company_user = User.objects.create_user(username="1234567891", password="123456", first_name="محمد", last_name="محمدی",
                                                    phone=9123456789, bank_account_number="520560611828005124784801", cash=1000000, type=1, is_active=True)
            self.stdout.write("company created %s" % company_user.username)
        except:
            self.stdout.write("company already created")
        try:
            vendor_user = User.objects.create_user(username="1234567892", password="123456", first_name="احمد",
                                                   last_name="احمدی", phone=9124578958, bank_account_number="520560611828005124784802", type=2, is_active=True)
            self.stdout.write("Vendor created %s" % vendor_user.username)
        except:
            self.stdout.write("Vendor already created")
        try:
            insured_user = User.objects.create_user(username="1234567894", password="123456", first_name="قاسم",
                                                    last_name="قاسمی", phone=9128564789, bank_account_number="520560611828005124784805", type=5, is_active=True)
            insured_object = Insured.objects.create(user=insured_user)
            self.stdout.write("Insured created %s" %
                              insured_object.user.username)
        except:
            self.stdout.write("Insured already created")
        try:
            holder_user = User.objects.create_user(username="1234567895", password="123456", first_name="محمود",
                                                   last_name="محمودی", phone=9128630215, bank_account_number="520560611828005124784804", type=4, is_active=True)
            holder_instance = Insured.objects.create(user=holder_user)
            holder_instance.supported_insureds.add(insured_user)
            self.stdout.write("Holder created %s" %
                              holder_instance.user.username)
        except:
            self.stdout.write("Holder already created")

        try:
            superholder_user = User.objects.create_user(username="1234567893", password="123456", first_name="ناصر",
                                                        last_name="ناصری", phone=912502154, bank_account_number="520560611828005124784803", type=3, is_active=True)
            superholder_instance = SuperHolder.objects.create(
                user=superholder_user)
            superholder_instance.supported_holders.add(holder_user)
            self.stdout.write("SuperHolder created %s" %
                              superholder_instance.user.username)
        except:
            self.stdout.write("SuperHolder already created")

    def create_insurance(self):
        try:
            insurance = Insurance.objects.create(
                name="بیمه درمانی", price=100000, description="بیمه درمانی برای بیماران بیمه درمانی", claim_form="", register_form="")
            self.stdout.write("Insurance created %s" % insurance.name)
        except:
            self.stdout.write("Insurance already created")

        Insurance.objects.create(
            name="4بیمه شخص ثالث", description="پرداخت هزینه های مربوط به تصادفات و خسارات ناشی از سوانح", price=10000000,
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
        try:
            self.create_users()
        except:
              self.stdout.write("Users have already been created")
        try:
            self.create_insurances()
        except:
            self.stdout.write("Insurances have already been created")
        try:
            self.create_claims()
        except:
            self.stdout.write("Users have already been created")
        self.create_tickets()
