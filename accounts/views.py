from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View

class RegisterView(View):

    def get(self, request):
        return render(request, 'accounts/register.html')


    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            u = User(username=username, email=email)
            u.set_password(password)
            u.save()
            return redirect('home')

        return render(request, 'accounts/register.html',{'error':'Passwords do not match'})


class LoginView(View):

    def get(self, request):
        return render(request, 'accounts/login_form.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        next_url = request.GET.get('next', 'home')
        if user is not None:
            login(request, user)
            return redirect(next_url)
        return render(request, 'accounts/login_form.html', {"error":"Invalid username or password"})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')



class ChangePasswordView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'accounts/change_password.html')

    def post(self, request):
        username = request.user.username
        old_password = request.POST['old_password']
        password = request.POST['password']
        password2 = request.POST['password2']
        user = authenticate(username=username, password=old_password)
        if user is not None:
            if password == password2:
                user.set_password(password)
                user.save()
                return redirect('home')
        return render(request, 'accounts/change_password.html', {"error":"jakiś error"})