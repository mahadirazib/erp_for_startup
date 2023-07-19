from django import forms
from .models import clientAndServiceProvider
from userAuth import models


class registerEntity(forms.ModelForm):
    isClient = forms.BooleanField(label='Is this entity a client', required=False)
    class Meta():
        model = clientAndServiceProvider
        fields = ('isClient', 'name', 'phone', 'email', 'occupation', 'companyName' )
