from django.dispatch import receiver
from django.db.models.signals import post_save
from leave.models import EmployeeLeave, LeaveRequest
from notification.models import Notification


@receiver(post_save, sender=LeaveRequest)
def notify_supervisor(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient = instance.supervisor,
            sender = instance.employee,
            message = f'{instance.employee} has a request for {instance.leave_type.leave_type}, Please review.',
            status = 'unread'
        )


@receiver(post_save, sender=LeaveRequest)
def notify_employee(sender, instance, created, **kwargs):
    if not instance.is_pending():
        if instance.leave_request_status == 'approved':
            message  = f'Your {instance.leave_type.leave_type} request has been approved.'
        else:
            message  = f'Your {instance.leave_type.leave_type} request has been rejected.'
        Notification.objects.create(
            recipient = instance.employee,
            sender = instance.supervisor,
            message = message,
            status = 'unread'
        )

@receiver(post_save, sender=LeaveRequest)
def update_leave_balance(sender, instance, created, **kwargs):
    if not created and instance.leave_request_status == 'approved':
        leave_id = instance.leave_type.id
        employee_leave = EmployeeLeave.objects.get(id=leave_id)
        employee_leave.leave_balance = instance.leave_type.leave_balance - instance.leave_duration
        employee_leave.save(update_fields=['leave_balance'])
        print('Your leave request has been approved')
