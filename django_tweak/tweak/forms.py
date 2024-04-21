from django.forms import ModelForm
from tweak.models import Employee
from django import forms


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        
        widgets = {
            'dob': forms.DateInput(attrs={ 'type': 'date', 'placeholder': 'Date of Birth'}),
            # 'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            # 'sex': forms.RadioSelect(attrs={'placeholder': ''}),
            # 'hobbie': forms.SelectMultiple(attrs = {'type':' checkbox',})
        }
        # all field mentioned here, with value '' will be shown without label
        labels = {
            # 'dob': '',
        }
        # exclude = ['hobbie', ]

