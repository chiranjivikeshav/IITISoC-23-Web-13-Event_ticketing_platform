from django.db import models
from django.contrib.auth.models import User
from organizer.models import Eventdetails,Ticket
import datetime

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
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=True)
    event = models.ForeignKey(Eventdetails, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    paymentStatus  =  models.BooleanField(default=False)
    



class Attendee(models.Model):
    event = models.ForeignKey(Eventdetails, on_delete=models.CASCADE,default=True)
    cartitem = models.ForeignKey(CartItem, on_delete=models.CASCADE,default=True)
    attendeName = models.CharField( max_length=50)
    attendeEmail = models.EmailField(max_length=30)
    attendeGender = models.CharField(max_length=10)
    attendeAddress = models.CharField(max_length=50)
    attendeContact = models.PositiveIntegerField()
    attendeCountry = models.CharField(max_length=20)
    attendeState = models.CharField(max_length=20)
    attendeZIP = models.PositiveIntegerField()
    timeStamp=models.DateTimeField(blank=True,null=True,default=datetime.datetime.now())
    payment_id = models.CharField(max_length=100,default=True)
    