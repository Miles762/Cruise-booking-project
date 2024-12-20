from django import forms
from .models import Stateroom, Side, Package

class PassengerForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=30)
    state = forms.CharField(max_length=30)
    country = forms.CharField(max_length=30)
    zip_code = forms.CharField(max_length=10)
    phone_number = forms.CharField(max_length=15)
    blood_group = forms.ChoiceField(choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
    ])

class StateroomSelectionForm(forms.Form):
    def __init__(self, *args, num_passengers=1, **kwargs):
        super().__init__(*args, **kwargs)
        if num_passengers > 4:
            queryset = Stateroom.objects.filter(number_of_bed=6)
        elif num_passengers > 3:
            queryset = Stateroom.objects.filter(number_of_bed__in=[4, 6])
        elif num_passengers > 1:
            queryset = Stateroom.objects.filter(number_of_bed__in=[2, 4, 6])
        else:
            queryset = Stateroom.objects.filter(number_of_bed__in=[1, 2, 4, 6])
        self.fields['stateroom'] = forms.ModelChoiceField(queryset=queryset)
        print(queryset)
    side = forms.ModelChoiceField(queryset=Side.objects.all())

class PackageSelectionForm(forms.Form):
    packages = forms.ModelMultipleChoiceField(queryset=Package.objects.all(), widget=forms.CheckboxSelectMultiple)
