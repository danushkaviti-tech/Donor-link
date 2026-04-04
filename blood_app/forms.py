from django import forms
from django.contrib.auth.models import User
from .models import Donor, Hospital

# Choice list for the dropdown
BLOOD_GROUPS = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]

class DonorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'rounded-pill'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class DonorProfileForm(forms.ModelForm):
    # Using Select widget for the dropdown
    blood_group = forms.ChoiceField(choices=BLOOD_GROUPS, widget=forms.Select(attrs={'class': 'form-select'}))
    
    class Meta:
        model = Donor
        fields = ['blood_group', 'location', 'phone']

class HospitalRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'rounded-pill'}))
    # Using a standard Textarea for the address
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    # We add 'address' manually to the form because it's not in the User model
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'] = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))