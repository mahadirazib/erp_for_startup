from django import forms
from .models import notice
from userAuth import models


class addNotice(forms.ModelForm):

    deadLine = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), required=False)
    class Meta():
        model = notice
        fields = ('user', 'title', 'details', 'needToComplete', 'deadLine')
        

    def __init__(self, *args, **kwargs): 
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        self.css_class = "formInput"
        self.fields['user'].label = 'For Whom'
        self.fields['title'].label = 'Notice Title'
        self.fields['title'].widget.attrs = ({'type': 'password'})
        self.fields['details'].label = 'Notice Detailes'
        self.fields['needToComplete'].label = 'Is it a work that needs to be completed'




class editNotice(forms.ModelForm):
    
    deadLine = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), required=False)
    class Meta():
        model = notice
        fields = ('user', 'title', 'details', 'needToComplete', 'deadLine', 'completedBy')

    def __init__(self, *args, **kwargs): 
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.css_class = "formInput"
        self.fields['user'].label = 'For Who'
        self.fields['title'].label = 'Notice Title'
        self.fields['details'].label = 'Notice Detailes'
        self.fields['needToComplete'].label = 'Is it a work that needs to be completed'






