from django.db import models
from employee.models import Employee
from setting.models import Holiday, WorkSchedule
import numpy as np


class LeaveType(models.Model):
    LEAVE_TYPE = (
        ('annual leave', 'Annual Leave'),
        ('paternity leave', 'Paternity Leave'),
        ('maternity leave', 'Maternity Leave'),
        ('sick leave', 'Sick Leave'),
        ('study leave', 'Study Leave'),
        ('unpaid leave', 'Unpaid Leave'),
        ('compensatory time off', 'Compensatory time Off'),
        ('compassionate leave', 'compassionate Leave'),
    )
    leave_type = models.CharField(choices = LEAVE_TYPE, max_length=150, unique=True)
    number_of_leave_days = models.IntegerField()
    carryover_unused = models.BooleanField()
    employee_leave = models.ManyToManyField(Employee, through='Employeeleave',  through_fields=('leave_type','employee'),related_name='employee_leaves')

    def __str__(self) -> str:
        return self.leave_type
    

class EmployeeLeave(models.Model):
    LEAVE_STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    leave_balance = models.IntegerField(blank=True, null=True) #calculated field type FloatField
    leave_status = models.CharField(max_length=100, choices=LEAVE_STATUS)

    class Meta:
        unique_together = ('leave_type','employee')
    
    # def save(self, *args, **kwargs ):
    #     if self.leave_type.leave_type == 'Annual Leave':
    #         self.leave_balance = 0
    #     super(EmployeeLeave, self).save( *args, **kwargs)

    def __str__(self) -> str:
        return f'{self.employee} - {self.leave_type.leave_type}'


class LeaveRequest(models.Model):
    APPLICATION_STATUS = (
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(EmployeeLeave, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date =models.DateField()
    acting_staff = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='acting_employee', blank=True, null=True)
    employee_note = models.TextField() 
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_supervisor', blank=True, null=True)
    supervisor_comment = models.TextField()
    leave_request_status = models.CharField(max_length=100, choices=APPLICATION_STATUS, default = 'pending')

    def is_pending(self):
        return self.leave_request_status == 'pending'

    def __str__(self):
        return f'{self.leave_type.leave_type} - {self.leave_request_status}'
    
    @property
    def leave_duration(self):
        holidays = Holiday.objects.all()
        holiday_dates = []
        for holiday in holidays:
            holiday_dates.append(holiday.holiday_date)
        return np.busday_count(self.start_date, self.end_date, holidays=holiday_dates) + 1
    