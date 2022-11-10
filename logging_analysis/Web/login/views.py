import hashlib

from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET

from Web.utils import *
from login.models import User
# Create your views here.


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


@require_http_methods(['POST', 'GET'])
def login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
    else:
        user_id = request.POST.get('id')
        password = request.POST.get('password')
        try:
            user = User.objects.get(user_id=user_id)
        except Exception as e:
            print(e)
            user = None
        if user is not None:
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['id'] = user.id
                request.session['user_id'] = user.user_id
                days = request.GET.get("days", 365)
                x_data, record_data = get_records(days)
                total = get_total_records(days)
                users_count = get_records_by_user(days)
                types_count = get_records_by_type(days)
                return render(request, "dashboard.html", locals())
            else:
                return render(request, 'login/login.html', {"message": "Password is error"})
        else:
            return render(request, 'login/login.html', {"message": "Account is not exist"})


@require_http_methods(['POST', 'GET'])
def register(request):
    if request.method == 'GET':
        return render(request, 'login/register.html')
    else:
        user_id = request.POST.get('id')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password != password_confirm:
            return render(request, 'login/register.html', {"message": "The two passwords do not match"})
        else:
            same_name_user = User.objects.filter(user_id=user_id)
            if same_name_user:
                return render(request, 'login/register.html', {"message": "The user name is exist"})
            same_email_user = User.objects.filter(email=email)
            if same_email_user:
                return render(request, 'login/register.html', {"message": "The email is registered"})

            new_user = User.objects.create()
            new_user.user_id = user_id
            new_user.full_name = full_name
            new_user.email = email
            new_user.password = hash_code(password)
            new_user.save()
            return render(request, 'login/login.html')


@require_http_methods(['POST', 'GET'])
def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'login/forgot-password.html')
    else:
        user_id = request.POST.get('id')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password != password_confirm:
            return render(request, 'login/forgot-password.html', {"warning": "The two passwords do not match"})
        else:
            user = User.objects.get(user_id=user_id)
            user.password = hash_code(password)
            user.save()
            return render(request, 'login/forgot-password.html', {"info": "The password is reset"})


@require_GET
def logout(request):
    request.session.flush()
    return render(request, 'login/login.html')
