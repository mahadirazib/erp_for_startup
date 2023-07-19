from django import forms
from django.contrib.auth.models import User
from .models import userInfo


class userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type':'password'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')




class userformMoreinfo(forms.ModelForm):

    class Meta():
        model = userInfo
        fields = ('phone', 'gender', 'role', 'bloodGroup', 'proPic', 'fbLink')

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['proPic'].label = 'Profile pic'
        self.fields['fbLink'].label = 'Facebook Profile'





