from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import *
from django.views.decorators.csrf import csrf_exempt
# from django.contrib import admin

urlpatterns = [
    path('', views.registerPage, name='register'),
    path('email_confirm/', views.emailConfirm, name='confirm_email'),
    path('login/', views.loginPage, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path ('reset_password/', auth_views.PasswordResetView.as_view(
    						template_name='registration/reset_password.html'), 
    						name="password_reset"),

    path ('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
    						template_name='registration/password_reset_sent.html'), 
    						name="password_reset_done"),

    path ('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    						template_name='registration/password_reset_id.html'), 
    						name="password_reset_confirm"),

    path ('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
    						template_name='registration/password_reset_com.html'), 
    						name="password_reset_complete"),

    path ('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_com.html'), name="password_reset_complete"),

    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate')

    
]
