from django.core.management.base import BaseCommand
from authenticate.models import User
from insured.models import Insured
from super_holder.models import SuperHolder

class Command(BaseCommand):
    """
    creates some database objects to for development and testing
    """

    def handle(self, *args, **kwargs):
        User.objects.create(username="1234567891", password="123456", first_name="محمد", last_name="محمدی",
                            phone=9123456789, bank_account_number=520560611828005124784801, type="Company", is_active=True, is_superuser=True, is_staff=True)
        self.stdout.write("company created 1234567891")

        User.objects.create(username="1234567892", password="123456", first_name="احمد", last_name="احمدی",
                            phone=9123456789, bank_account_number=520560611828005124784802, type="Vendor", is_active=True, is_superuser=True, is_staff=True)
        self.stdout.write("Vendor created 1234567892")

        User.objects.create(username="1234567894", password="123456", first_name="قاسم", last_name="قاسمی",
                            phone=9123456789, bank_account_number=520560611828005124784805, type="Insured", is_active=True, is_superuser=True, is_staff=True)
        Insured.objects.create(user=User.objects.get(username="1234567894"))
        self.stdout.write("Insured created 1234567894")

        User.objects.create(username="1234567895", password="123456", first_name="محمود", last_name="محمودی",
                            phone=9123456789, bank_account_number=520560611828005124784804, type="Holder", is_active=True, is_superuser=True, is_staff=True)
        Insured.objects.create(user=User.objects.get(username="1234567895"),supported_insureds=Insured.objects.get(user=User.objects.get(username="1234567894")))
        self.stdout.write("Holder created 1234567895")

        User.objects.create(username="1234567893", password="123456", first_name="ناصر", last_name="ناصری",
                            phone=9123456789, bank_account_number=520560611828005124784803, type="SuperHolder", is_active=True, is_superuser=True, is_staff=True)
        SuperHolder.objects.create(user=User.objects.get(username="1234567893"),supported_holders=Insured.objects.get(user=User.objects.get(username="1234567895")))
        self.stdout.write("SuperHolder created 1234567893")
