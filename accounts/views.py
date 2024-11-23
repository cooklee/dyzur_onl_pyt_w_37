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
