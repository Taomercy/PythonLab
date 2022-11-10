"""Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path, include
from login.views import login
from Web.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', login, name='login'),
    path('login/', include('login.urls', namespace="login")),

    path('api/', include('rest.urls', namespace="rest")),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    re_path(r'^results_display', results_display, name='results_display'),
    re_path(r'^dashboard', dashboard, name='dashboard'),
    re_path(r'^MHWeb_display', MHWeb_display, name='MHWeb_display'),
    re_path(r'^case_display', case_display, name='case_display'),
    re_path(r'^upload_case', upload_case, name='upload_case'),
    re_path(r'^delete_case', delete_case, name='delete_case'),
    re_path(r'^download_case', download_case, name='download_case'),

    re_path(r'^app_log_type_display', app_log_type_display, name='app_log_type_display'),
    re_path(r'^create_applog_type', create_applog_type, name='create_applog_type'),
    re_path(r'^delete_app_type', delete_app_type, name='delete_app_type'),
    re_path(r'^test_case_check', test_case_check, name='test_case_check'),
    re_path(r'^result_details', result_details, name='result_details'),
    re_path(r'^delete_result', delete_result, name='delete_result'),
    # re_path(r'^check_app_log', check_app_log, name='check_app_log'),
    re_path(r'^property_display', property_display, name='property_display'),
    re_path(r'^create_property', create_property, name='create_property'),
    re_path(r'^delete_property', delete_property, name='delete_property'),
    re_path(r'^modify_property', modify_property, name='modify_property'),
    re_path(r'^time_axis', time_axis, name='time_axis'),
]
