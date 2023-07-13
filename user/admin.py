from django.contrib import admin
from .models import Userprofile,CartItem
# Register your models here.
admin.site.register(Userprofile)
admin.site.register(CartItem)