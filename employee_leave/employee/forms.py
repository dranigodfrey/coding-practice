from django.forms import ModelForm
from employee.models import Employee


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        # exclude = ('user','supervisor',)

        