from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Shift(models.Model):
    date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.owner} {self.date}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'date'],name='unique_shift_owner'),
        ]


class ChangeShiftProposal(models.Model):
    from_shift = models.OneToOneField(Shift, on_delete=models.CASCADE, null=True,
                                   related_name='from_shift')
    to_shift = models.OneToOneField(Shift, on_delete=models.CASCADE, null=True,
                                 related_name='to_shift')
    accepted = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    date_of_acceptance = models.DateField(auto_now=True)








