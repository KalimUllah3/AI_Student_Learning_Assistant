from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse
from django.contrib.auth import logout

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})
def home(request):
    return HttpResponse("""
    <h1>Welcome to AI Student Learning Assistant</h1>
    <br>
    <a href='/logout/'>Logout</a>
    """)
def logout_view(request):
    logout(request)
    return redirect('login')