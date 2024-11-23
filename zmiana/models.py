from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Shift(models.Model):
    date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)