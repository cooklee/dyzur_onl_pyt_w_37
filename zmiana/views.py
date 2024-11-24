
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import  HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from zmiana.models import Shift


class MyLoginRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'musisz być zalogowany')
        return super().dispatch(request, *args, **kwargs)
# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, template_name='base.html')


class MyDuty(MyLoginRequiredMixin, View):
    def get(self, request):
        shifts = Shift.objects.filter(owner=request.user).order_by('date')
        return render(request, template_name='zmiana/my_duty.html',context={'shifts':shifts})


class AddNewShiftView(MyLoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name='zmiana/add_new_shift.html')

    def post(self, request):
        user = request.user
        date = request.POST['date']
        Shift.objects.create(owner=user, date=date)
        return redirect('add_new_shift')



class DutyProposal(View):
    def get(self, request):
        return render(request, template_name='zmiana/duty_proposal.html')