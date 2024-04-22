from django.db import models
from datetime import datetime
from multiselectfield import MultiSelectField

# Create your models here.
class Employee(models.Model):
    SEX = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    HOBBIE = (
        ('football', 'Football'),
        ('reading', 'Reading'),
        ('Swimming', 'Swimming'),
    )
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    dob = models.DateField()
    sex = models.CharField(max_length=10, choices=SEX,)
    hobbie = MultiSelectField(choices=HOBBIE, max_length=125, max_choices = 2, default=None)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    @property
    def age(self):
       return datetime.now().year - self.dob.year