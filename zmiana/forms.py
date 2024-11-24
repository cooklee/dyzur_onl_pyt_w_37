from django import forms

from zmiana.models import Shift


class ChangeShiftForm(forms.Form):
    from_shift = forms.ModelChoiceField(queryset=Shift.objects.all())
    to_shift = forms.ModelChoiceField(queryset=Shift.objects.all())

    def __init__(self, *args,user=None, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['from_shift'].queryset=Shift.objects.filter(owner=user, active=True)
        qs = Shift.objects.filter(active=True)
        self.fields['to_shift'].queryset=qs.exclude(owner=user)
