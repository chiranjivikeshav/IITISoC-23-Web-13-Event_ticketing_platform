from django.contrib import admin
from .models import Eventdetails,Ticket,Organizer
# Register your models here.
admin.site.register(Eventdetails)
admin.site.register(Ticket)
admin.site.register(Organizer)