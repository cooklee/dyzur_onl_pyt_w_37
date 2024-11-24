from django import forms
from django.core.exceptions import ValidationError

from zmiana.models import Shift, Person


def check_letter(value):
    if not value[0].isupper():
        raise ValidationError("Tylko wielka litera")

def check_end(value):
    if value[-1] != 'k':
        raise ValidationError("Musi konczyć sie na K")

class ChangeShiftForm(forms.Form):
    # name = forms.CharField(max_length=8, validators=[check_letter, check_end])
    from_shift = forms.ModelChoiceField(queryset=Shift.objects.all())
    to_shift = forms.ModelChoiceField(queryset=Shift.objects.all())

    def __init__(self, *args,user=None, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['from_shift'].queryset=Shift.objects.filter(owner=user, active=True)
        qs = Shift.objects.filter(active=True)
        self.fields['to_shift'].queryset=qs.exclude(owner=user)


class AddPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Imię',
        }


