from django.db import models


class Holiday(models.Model):
    holiday_name = models.CharField(max_length=150)
    holiday_date = models.DateField()
    updated_date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.holiday_name
    

class WorkSchedule(models.Model):
    WEEK_DAY =(
        ('sun','Sunday'),
        ('mon','Monday'),
        ('tue','Tuesday'),
        ('wed','Wednesday'),
        ('thur','Thursday'),
        ('fri','Friday'),
        ('sat', 'Saturday'),
    )

    STATUS = (
        ('workday', 'Work Day'),
        ('offday', 'Off Day')
    )
    week_day = models.CharField(max_length=100, choices=WEEK_DAY)
    time_start = models.TimeField()
    time_end = models.TimeField()
    status = models.CharField(max_length=100, choices=STATUS)

    def __str__(self) -> str:
        return f'{self.week_day} {self.status}'