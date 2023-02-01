from django import forms
from . import models


class registerNewDeals(forms.ModelForm):
    dealEnds = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta():
        model = models.currentDeals
        fields = '__all__'

    def __init__(self, *args, **kwargs): 
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['whoCanSee'].label = 'Who can See this Deal'
        self.fields['giveOrReceive'].label = 'Give or Recive'
        self.fields['dealWith'].label = 'Deal With'
        self.fields['dealAmount'].label = 'Deal Amount'
        self.fields['dealTitle'].label = 'Deal Title'
        self.fields['dealDescription'].label = 'Describe your deal here'
        self.fields['dealEnds'].label = 'Deal Ends'