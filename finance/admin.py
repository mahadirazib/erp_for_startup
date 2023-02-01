from django.contrib import admin
from .models import salary, paidUnpaidSalaryStatus, clientAndServiceProvider, recivedMoney, spendMoney

# Register your models here.

admin.site.register(salary)
admin.site.register(paidUnpaidSalaryStatus)
admin.site.register(clientAndServiceProvider)
admin.site.register(recivedMoney)
admin.site.register(spendMoney)
