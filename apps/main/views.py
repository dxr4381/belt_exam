from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, 'main/index.html')

def create_user(request):
    if len(request.POST.get('name')) < 0:
        messages.error(request, "Name must be Valid")
    if len(request.POST.get('email')) < 0:
        messages.error(request, 'Email must be Valid')
    if len(request.POST.get('password')) < 7:
        messages.error(request, 'Password must contain at least 7 characters')
    elif not EMAIL_REGEX.match(request.POST.get('email')):
        messages.error(request, 'Please enter the Email in valid form')
        return redirect('/')
    is_valid = User.objects.validate_user(request.POST)
    if is_valid[0]:
        user = User.objects.create(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            password = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt()),
        )
        request.session['user_id'] = user.id
        return redirect('/success')
    else:
        for error in is_valid[1]:
            messages.error(request, error)
        return redirect('/')

def login_user(request):
    if request.method == 'POST':
        login = User.objects.login_user(request.POST)
        if login[0]:
            request.session['user_id']=login[1].id
            return redirect('/success')
        else:
            messages.error(request,"Login not found. Please make another account.")
        return redirect('/')

def log_out(request):
    request.session.clear()
    return redirect('/')

def success(request):
    favorite = []
    fav_list = Favorite.objects.filter(user= request.session['user_id'])
    for fav in fav_list:
        favorite.append(fav.quote.id)
        favorite.append(request.session['user_id'])
    context = {
        'current_user':User.objects.get(id=request.session['user_id']),
        'quotes':Quote.objects.exclude(id__in=favorite),
        'favorites':Favorite.objects.filter(user=request.session['user_id']),
        # 'fav_quote':Quote.objects.exclude(id__in=favorite),had to combine this becasue it with quotes
        'user':User.objects.exclude(id=request.session['user_id'])
    }
    return render(request, 'main/success.html', context)

def submit(request):
    if len(request.POST.get('quoted_by')) < 3:
        messages.error(request, 'Quoted by must contain 3 characters')
    elif len(request.POST.get('message')) < 10:
        messages.error(request, 'Message must contain 10 characters')
    else:
        Quote.objects.create(
            user = User.objects.get(id=request.session['user_id']),
            author= request.POST.get('quoted_by'),
            quote= request.POST.get('message'),
        )
    return redirect('/success')

def list(request, id):
    Favorite.objects.create(
        user = User.objects.get(id=request.session['user_id']),
        quote = Quote.objects.get(id=id)
    )
    return redirect('/success')

def remove(request, id):
    Favorite.objects.filter(quote__id = id).delete()
    return redirect('/success')

def profile(request, id):
    context = {
        'user':Quote.objects.filter(user = id).first(),
        'quotes':Quote.objects.filter(user = id),
        'count':len(Quote.objects.filter(user = id))

    }
    return render(request, 'main/profile.html', context)

def home(request):
    return redirect('/success')
