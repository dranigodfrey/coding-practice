from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

