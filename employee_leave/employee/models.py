from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
class Employee(models.Model):
    SEX = (
        ('male', 'Male'),
        ('female','Female'),
    )

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    employee_firstname = models.CharField(max_length=20)
    employee_lastname = models.CharField(max_length=20)
    employee_email = models.EmailField()
    employee_dob = models.DateField(blank=True, null=True)
    employee_sex = models.CharField(max_length=10, choices=SEX)
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
  
    
    def __str__(self) -> str:
        return f'{self.employee_firstname} {self.employee_lastname}'

    

