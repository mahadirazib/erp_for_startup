from django.db import models
from django.contrib.auth.models import User
from userAuth.models import userInfo

# Create your models here.

class salary(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salary = models.IntegerField()



class paidUnpaidSalaryStatus(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthlySalary = models.IntegerField()
    month = models.DateField()
    paidStatus = models.BooleanField()



class clientAndServiceProvider(models.Model):

    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    occupation = models.CharField(max_length=50, blank=True)
    companyName = models.CharField(max_length=50, blank=True)
    isClient = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name + ' (' + self.companyName + ')'



class recivedMoney(models.Model):

    recivedFrom = models.ForeignKey(clientAndServiceProvider, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField()
    purpose = models.CharField(max_length=50)
    medium = models.CharField(max_length=30)

    
    

class spendMoney(models.Model):

    spendOn = models.ForeignKey(clientAndServiceProvider, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField()
    purpose = models.CharField(max_length=50)
    medium = models.CharField(max_length=30)


    







