
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.http import  HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView

from zmiana.forms import ChangeShiftForm, AddPersonForm
from zmiana.models import Shift, ChangeShiftProposal, Person


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
        shifts = Shift.objects.filter(owner=request.user, active=True).order_by('date')
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
    #class DutyProposal(PermissionRequiredMixin, View):
    # permission_required = ['zmiana.change_shift']
    def get(self, request):
        return render(request, template_name='zmiana/duty_proposal.html')


class ShiftChangeProposalView(MyLoginRequiredMixin, View):

    def get(self, request):
        form = ChangeShiftForm(user=request.user)
        return render(request, 'form.html', {'form': form})


    def post(self, request):
        form = ChangeShiftForm(request.POST, user=request.user)
        if form.is_valid():
            from_shift = form.cleaned_data['from_shift']
            to_shift = form.cleaned_data['to_shift']
            csp = ChangeShiftProposal(from_shift=from_shift, to_shift=to_shift)
            csp.save()
            return redirect('home')
        return render(request, 'form.html', {'form': form})


class MyShiftProposalView(MyLoginRequiredMixin, View):

    def get(self, request):
        requested_proposals = ChangeShiftProposal.objects.filter(to_shift__owner=request.user, accepted=False).order_by('date')
        my_proposal = ChangeShiftProposal.objects.filter(from_shift__owner=request.user, accepted=False).order_by('date')
        return render(request,
                      'zmiana/shift_proposal_view.html', {'requested_proposals':requested_proposals,
                                                          'my_proposal':my_proposal})


class AcceptProposalView(UserPassesTestMixin, View):

    def test_func(self):
        pk = self.kwargs['pk']
        csp = ChangeShiftProposal.objects.get(pk=pk)
        return csp.to_shift.owner == self.request.user


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


class AddPersonView(View):
    def get(self, request):
        form = AddPersonForm()
        return render(request, 'form.html', {'form':form})

    def post(self, request):
        form = AddPersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            return redirect('home')
        return render(request, 'form.html', {'form': form})


class AddPersonViewGeneric(CreateView):
    model = Person
    form_class = AddPersonForm
    success_url = reverse_lazy('home')
    template_name = 'form.html'

class UpdatePersonView(UpdateView):
    model = Person
    form_class = AddPersonForm
    success_url = reverse_lazy('home')
    template_name = 'form.html'

class DetailPersonView(DetailView):
    model = Person
    template_name = 'cos.html'

class PersonListView(ListView):
    model = Person
    template_name = 'person_list.html'

class DeletePersonView(DeleteView):
    model = Person
    success_url = reverse_lazy('home')
    template_name = 'confirm_delete.html'


