"""
URL configuration for dyzury project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from zmiana import views
from accounts import views as accounts_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='home'),
    path('my_duty/', views.MyDuty.as_view(), name='my_duty'),
    path('duty_proposal/', views.DutyProposal.as_view(), name='duty_proposal'),
    path('register/', accounts_views.RegisterView.as_view(), name='register'),
    path('login/', accounts_views.LoginView.as_view(), name='login'),
    path('logout/', accounts_views.LogoutView.as_view(), name='logout'),
    path('change_password/', accounts_views.ChangePasswordView.as_view(), name='change_password'),

    path('add_new_shift/', views.AddNewShiftView.as_view(), name='add_new_shift'),
    path('change_shift_proposal/', views.ShiftChangeProposalView.as_view(), name='change_shift_proposal'),
    path('my_shift_proposal/', views.MyShiftProposalView.as_view(), name='my_shift_proposal'),
    path('proposal/<int:pk>/accept/', views.AcceptProposalView.as_view(), name='proposal_accept'),
]
