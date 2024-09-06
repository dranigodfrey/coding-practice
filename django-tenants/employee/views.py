from django.shortcuts import render
from employee.models import Employee
# Create your views here.

def employee(request):
    employee = Employee.objects.all()
    return render(request, 'employee/employee.html', {'employees': employee})