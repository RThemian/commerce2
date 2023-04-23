from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm
# auth_views is a module that contains all the views for authentication
# we are importing the LoginView class from the module


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    # need log out, but redirect to login page not admin page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

     # how can I change where the LogoutView redirects to? 
]
