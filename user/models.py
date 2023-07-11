from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=30)
    user_about = models.TextField()
    contact_number = models.CharField(max_length=15)
    user_email = models.EmailField()
    user_weburl = models.CharField(max_length=100)
    user_fburl = models.CharField(max_length=100)
    user_twurl = models.CharField(max_length=100)
    user_ldurl = models.CharField(max_length=100)
    def __str__(self):
        return self.user_name

