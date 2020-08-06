from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def registerPage(request):

    # CreateUserForm() - imported from forms.py
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        # Form validation & save
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')

            # flash message
            messages.success(request, 'Account was created successfully for ' + user)
            return redirect('login')
            
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def loginPage(request):

    # Fetching request method, username & password
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticating user
        user = authenticate(request, username=username, password=password)

        # Checking if user exist
        if user is not None:
            login(request, user)
            return redirect ('dashboard')
        else:
            messages.info(request, 'Username or Password is Incorrect')
    return render(request, 'registration/login.html')

def dashboard(request):
    return render(request, 'registration/dashboard.html')