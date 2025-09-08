from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    USER_ROLES=(
        ('student','Student'),
        ('admin','Admin'),
    )
    role=models.CharField(max_length=10,choices=USER_ROLES)

    def __str__(self):
     return f"{self.username}({self.role})"