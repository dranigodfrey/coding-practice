from django.contrib import admin
from leave.models import LeaveRequest, EmployeeLeave, LeaveType

# Register your models here.
admin.site.register(LeaveRequest)
admin.site.register(EmployeeLeave)
admin.site.register(LeaveType)