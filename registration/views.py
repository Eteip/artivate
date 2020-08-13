from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import CreateUserForm
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.core.mail import EmailMessage
import json
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, AbstractBaseUser   
from django.db import models
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import account_activation_token


def registerPage(request):

    # CreateUserForm() - imported from forms.py
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        # Get details
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1'] 

        # Form validation & save
        if form.is_valid():       
            # TODO:   fix condition - this code is not checking duplicate emails (as supposed)
            if not User.objects.filter(email=email).exists:
                print('\n\n\n\n\n\nCAUGHT')
                print(request)
                context = {'form': form}
                               
                return render(request, 'registration/register.html', context)

            # user = form.cleaned_data.get('username')
            # Checkiing for username and password
            user =  User.objects.create_user(username=username, email=email, password=password)

            email = form.cleaned_data.get('email')
            
            # Checkiing if user is active
            user.is_active = False
            print('\n\n\n\n\nuser.is_active: '+str(user.is_active))
            
            # Generating token - details gotten from utils.py
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            
            # getting te site adress to inject in to the toke
            domain = get_current_site(request).domain
            
            # constructing the token link. 
            # 'activate' is cominig from views.py, 
            # 'account_activation_token' is comming from utils.py using the .make_token() method
            link = reverse('activate', kwargs={'uidb64':uidb64, 'token': account_activation_token.make_token(user)})
            
            # activation link, concatinating domain
            activate_url = 'http://' + domain + link.lstrip('/')
            
            # Email body --->
            email_subject = 'Activate Your Account'
            email_body = 'Hi '+user.username + 'Please click on the link below to activate your account \n'+activate_url

            email = EmailMessage(
                email_subject,
                email_body,            
                'noreply@artivate.com',
                [email],
            )
            email.send(fail_silently=True)
            # Email body <---

            # Flash message
            messages.success(request, 'Account was created successfully for ' + str(user))
            return redirect('confirm_email')
        else:
            print('\n\n\n\n\n\n\n not valid')
            
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def emailConfirm(request):
    pass
    return render (request, 'registration/email_confirm.html')

class VerificationView(View):
    
    def get(self, request, uidb64, token): # this view is getting token and userid-uid
        
        # returning decoded user_id in pliain text
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)

        # print(user.is_active)
        user.is_active = True
        # print(user.is_active)
        # print('\n\npassed\n\n')

        
        user.save()
        # print('passed')
        messages.success(request, 'Account activated successfully')
        return redirect('login')
        # return redirect (request, 'login')

class LoginView(View):
    def get(self, request):
        return render (request, 'registration/login.html')


def loginPage(request):

    # Fetching request method, username & password
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticating user
        user = authenticate(request, username=username, password=password)
        # Checking if user exist
        if user is not None:
            print('\n\n\n'+str(user.is_active)+'\n\n\n')
            try:
                
                if user.is_active:
                    print('\n\npassedactive\n\n\n')
                    login(request, user)
                    print('\n\npassed\n\n\n')
                    return redirect ('dashboard')
                else:
                    return render(request, 'registration/dashboard.html')
            except:
                render(request, 'registration/dashboard.html')
        else:
            messages.info(request, 'Username or Password is Incorrect')
    return render(request, 'registration/login.html')

def dashboard(request):
    return render(request, 'registration/dashboard.html')

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})

