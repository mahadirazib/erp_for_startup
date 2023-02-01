from django.db import models
from finance.models import clientAndServiceProvider
from userAuth.models import userInfo

# Create your models here.


class currentDeals(models.Model):
    
    choise = (("give", "Give"), ("recive", "Recive"))

    whoCanSee = models.ManyToManyField(userInfo)
    giveOrReceive = models.CharField(max_length=10, choices=choise)
    dealWith = models.ForeignKey(clientAndServiceProvider, on_delete=models.CASCADE)
    dealAmount = models.IntegerField()
    dealTitle = models.CharField(max_length=100)
    dealDescription = models.TextField()
    dealEnds = models.DateField()




class allDealsRecord(models.Model):

    choise = (("give", "Give"), ("recive", "Recive"))
    giveOrReceive = models.CharField(max_length=10, choices=choise)
    dealWith = models.ForeignKey(clientAndServiceProvider, on_delete=models.CASCADE)
    dealAmount = models.IntegerField()
    dealTitle = models.CharField(max_length=100)
    dealDescription = models.TextField()
    dealEnds = models.DateField()
    completeOrTerminatedChoices = (('Completed', 'Completed'), ('Terminated', 'Terminated'))
    completeOrTerminated = models.CharField(max_length=10, choices=completeOrTerminatedChoices)

