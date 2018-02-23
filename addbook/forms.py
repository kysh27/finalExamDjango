from .models import UserProfile, AddressBook
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['fName'].label = "First Name"
        self.fields['lName'].label = "Last Name"
        self.fields['contactNum'].label = "Contact No."
        self.fields['address'].label = "Address"
        
    class Meta:
        model = AddressBook
        fields = ('fName', 'lName', 'contactNum', 'address',)