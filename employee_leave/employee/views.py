from django.shortcuts import render
from employee.forms import EmployeeForm
# from django.http import HttpResponse

# Create your views here.
def employee(request):
    form = EmployeeForm()
    context  ={
        'form': form
    }
    return render(request, template_name='employee/employee.html', context=context)