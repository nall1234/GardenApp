from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def index(request):
    if 'current_user' in request.session:
        return redirect ('/main')
    return render (request, 'index.html')

def login(request):
    if request.method == "POST":   
        if not User.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, 'Invalid Email/Password')
            return redirect('/')
        current_user = User.objects.get(email = request.POST['email'])
        request.session['current_user'] = current_user.id
        return redirect('/main')            
    else:
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def register(request):
    if request.method =="POST":
        errors = User.objects.user_validator(request.POST)        
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        password = request.POST['password']
        pwhash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pwhash
        )
        request.session['current_user'] = new_user.id
        return redirect('/main')
    else:
        return redirect("/")

def main(request):
    return render(request, 'main.html')