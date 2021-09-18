from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import *
from django.conf.urls import handler404


urlpatterns = [
    path('login/', signin, name='signin'),
    path('logout/', logoutuser, name='logout'),
    path('register/', signup, name='signup'),
    path('editprofile/<int:id>', editprofile, name='editprofile'),
    path('profile/<int:id>', infoprofile, name='profile'),



    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="password_reset"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),
] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)

handler404 = 'login.views.pagenotfound'
