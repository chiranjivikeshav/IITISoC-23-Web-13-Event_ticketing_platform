from django.db import models
from django.contrib.auth.models import User


class Organizer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    organizerName = models.TextField()
    organizerContact = models.TextField()
    organizerEmail = models.TextField()
    organizerAddress = models.TextField()
    organizerBankName = models.TextField()
    organizerBankBranch = models.TextField()
    organizerBankIFSC = models.TextField()
    organizerBankAccount = models.TextField()
    organizerAbout = models.TextField()
    def __str__(self):
        return self.organizerName





class Eventdetails(models.Model):
    eventOrganizer = models.ForeignKey(Organizer,on_delete=models.CASCADE,default=True)
    eventName = models.CharField(max_length=100)
    eventDisplay = models.CharField(max_length=100)
    eventStartDate = models.DateTimeField()
    eventEndDate = models.DateTimeField()
    eventAddress = models.CharField( max_length=50)
    eventCity = models.CharField( max_length=50)
    eventState = models.CharField( max_length=50)
    eventCountry = models.CharField( max_length=50)
    eventZip = models.IntegerField()
    eventDescription = models.CharField(max_length=3000)
    eventImage = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.eventName



class Ticket(models.Model):
    event = models.ForeignKey(Eventdetails, on_delete=models.CASCADE)
    ticketname = models.CharField(max_length=50)
    ticketprice = models.DecimalField(max_digits=8, decimal_places=2)
    ticketCount = models.PositiveIntegerField()
    def __str__(self):
        return self.event.eventName