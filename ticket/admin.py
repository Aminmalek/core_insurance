from django.contrib import admin
from .models import Claim, Ticket,ReviewerTimeline

admin.site.register(Ticket)
admin.site.register(Claim)
admin.site.register(ReviewerTimeline)