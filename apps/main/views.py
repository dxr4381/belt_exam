from django.shortcuts import render, redirect
from .models import *
import bcrypt

def index(request):
    return render(request, 'main/index.html')

def create_user(request):
    if User.objects.validate_user(request.POST):
        user = User.objects.create(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            password = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt()),
        )
        request.session['user_id'] = user.id
        return redirect('/success')
    return redirect('/')

def success(request):
    return render(request, 'main/success.html')

def login_user(request):
    login = User.objects.login_user(request.POST)
    if login[0]:
        request.session['user_id'] = login[1].id
        return redirect('/success')
    return redirect('/')
