from django.conf.urls import url
from django.contrib import admin
from login import views

app_name = 'login'

urlpatterns = [
    url(r'^login/', views.login, name="login"),
    url(r'^register/', views.register, name="register"),
    url(r'^forgot_password/', views.forgot_password, name="forgot_password"),
    url(r'^logout/', views.logout, name="logout"),
]