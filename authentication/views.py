from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate

# Create your views here.


def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            # handle login
            if request.POST['email'] and request.POST['password']:
                try:
                    user = User.objects.get(email=request.POST['email'])
                    usr = authenticate(username=user.username, password=request.POST['password'])
                    if usr is None:
                        messages.error(request, "Incorrect Email/Password")
                        return redirect(login)
                    auth.login(request, user)
                    if request.POST['next'] != '':
                        return redirect(request.POST.get('next'))
                    else:
                        return redirect('/')
                except User.DoesNotExist:
                    return render(request, 'login.html', {'error': "User Doesn't Exists"})
            else:
                return render(request, 'login.html', {'error': "Empty Fields"})
        else:
            return render(request, 'login.html')
    else:
        return redirect('/')


def signup(request):
    if request.method == 'POST':
        # sign in
        if request.POST['password'] == request.POST['password2']:
            if request.POST['username'] and request.POST['email'] and request.POST['password']:
                try:
                    user = User.objects.get(email=request.POST['email'])
                    return render(request, 'signup.html', {'error': "User Already Exists"})
                except User.DoesNotExist:
                    User.objects.create_user(
                        username=request.POST['username'],
                        email=request.POST['email'],
                        password=request.POST['password']
                    )
                    messages.success(request, "Signup Successful. Please Login Here")
                    return redirect(login)
            else:
                return render(request, 'signup.html', {'error': "Empty Fields"})
        else:
            return render(request, 'signup.html', {'error': "Passwords Don't Match"})
    else:
        return render(request, 'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

