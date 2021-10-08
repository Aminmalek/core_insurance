from django.contrib import admin
from .models import Claim, Ticket

admin.site.register(Ticket)
admin.site.register(Claim)