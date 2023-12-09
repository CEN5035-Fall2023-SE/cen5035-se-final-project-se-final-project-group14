from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import TaApplicant

from django.shortcuts import render, redirect
from .forms import TaApplicantForm

def signup(request):
    if request.method == 'POST':
        form = TaApplicantForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or login page
            return redirect('login')
    else:
        form = TaApplicantForm()

    return render(request, 'signup.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Replace 'dashboard' with the desired URL after login
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


