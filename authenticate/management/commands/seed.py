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

    def create_users(self):
        company_user = User.objects.create_user(username="1234567891", password="123456", first_name="محمد", last_name="محمدی",
                                           phone=9123456789, bank_account_number=520560611828005124784801, type="Company", is_active=True, is_superuser=True, is_staff=True)
        self.stdout.write("company created %s" % company_user.username)

        vendor_user = User.objects.create_user(username="1234567892", password="123456", first_name="احمد", last_name="احمدی",
                                          phone=9123456789, bank_account_number=520560611828005124784802, type="Vendor", is_active=True, is_superuser=True, is_staff=True)
        self.stdout.write("Vendor created %s" % vendor_user.username)

        insured_user = User.objects.create_user(username="1234567894", password="123456", first_name="قاسم", last_name="قاسمی",
                                           phone=9123456789, bank_account_number=520560611828005124784805, type="Insured", is_active=True, is_superuser=True, is_staff=True)
        insured_object = Insured.objects.create(user=insured_user)
        self.stdout.write("Insured created %s" % insured_object.user.username)

        holder_user = User.objects.create_user(username="1234567895", password="123456", first_name="محمود", last_name="محمودی",
                                          phone=9123456789, bank_account_number=520560611828005124784804, type="Holder", is_active=True, is_superuser=True, is_staff=True)
        holder_instance = Insured.objects.create(user=holder_user)
        holder_instance.supported_insureds.add(insured_user)
        self.stdout.write("Holder created %s" % holder_instance.user.username)
        # create a user
        User.objects.create_user
        superholder_user = User.objects.create_user(username="1234567893", password="123456", first_name="ناصر", last_name="ناصری",
                                               phone=9123456789, bank_account_number=520560611828005124784803, type="SuperHolder", is_active=True, is_superuser=True, is_staff=True)
        superholder_instance = SuperHolder.objects.create(
            user=superholder_user)
        superholder_instance.supported_holders.add(holder_user)
        self.stdout.write("SuperHolder created %s" %
                          superholder_instance.user.username)

    def create_tickets(self):
        pass

    def create_insurances(self):
        Insurance.objects.create(
            name="بیمه خسارات درمانی", type="درمانی", description="پرداخت هزینه های درمانی شامل هزینه های دارویی و بیمارستانی", price=10000000)
        Insurance.objects.create(
            name="بیمه شخص ثالث", type="درمانی", description="پرداخت هزینه های مربوط به تصادفات و خسارات ناشی از سوانح", price=10000000)
        self.stdout.write("insurances created")

    def handle(self, *args, **kwargs):
        self.create_users()
        self.create_tickets()
        self.create_insurances()
