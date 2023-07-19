from django.contrib import admin
from .models import currentDeals, allDealsRecord

# Register your models here.

admin.site.register(currentDeals)
admin.site.register(allDealsRecord)