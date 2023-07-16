from django.contrib import admin
from .models import Userprofile,CartItem,Attendee
# Register your models here.
admin.site.register(Userprofile)
admin.site.register(CartItem)
admin.site.register(Attendee)