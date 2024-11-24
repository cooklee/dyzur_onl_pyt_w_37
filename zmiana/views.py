
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import  HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from zmiana.forms import ChangeShiftForm
from zmiana.models import Shift, ChangeShiftProposal


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


class ShiftChangeProposalView(MyLoginRequiredMixin, View):

    def get(self, request):
        form = ChangeShiftForm(user=request.user)
        return render(request, 'zmiana/change_shift_form.html', {'form': form})


    def post(self, request):
        form = ChangeShiftForm(request.POST, user=request.user)
        if form.is_valid():
            from_shift = form.cleaned_data['from_shift']
            to_shift = form.cleaned_data['to_shift']
            csp = ChangeShiftProposal(from_shift=from_shift, to_shift=to_shift)
            csp.save()
            return redirect('home')
        return render(request, 'zmiana/change_shift_form.html', {'form': form})


class MyShiftProposalView(MyLoginRequiredMixin, View):

    def get(self, request):
        requested_proposals = ChangeShiftProposal.objects.filter(to_shift__owner=request.user).order_by('date')
        my_proposal = ChangeShiftProposal.objects.filter(from_shift__owner=request.user).order_by('date')
        return render(request,
                      'zmiana/shift_proposal_view.html', {'requested_proposals':requested_proposals,
                                                          'my_proposal':my_proposal})


class AcceptProposalView(MyLoginRequiredMixin, View):

    def get(self, request, pk):
        csp = ChangeShiftProposal.objects.get(pk=pk)

        csp.accepted = True
        csp.save()
        csp.to_shift.active = False
        csp.to_shift.save()
        csp.from_shift.active = False
        csp.from_shift.save()
        from_user = csp.from_shift.owner
        to_user = csp.to_shift.owner
        Shift.objects.create(owner=from_user, date=csp.to_shift.date)
        Shift.objects.create(owner=to_user, date=csp.from_shift.date)
        return redirect('my_duty')