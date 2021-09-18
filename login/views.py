from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

from blog.models import Post, Author, subscribe, Contact, Comment, SubComment

from .models import Userotp, profile
from .forms import *

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import *
from django.conf import settings
from .decorators import *
import random


# Create your views here.

@login_required(login_url='signin')
def home(request):
    return render(request, 'index.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    parms = {}
    return render(request, 'login.html', parms)


@login_required(login_url='signin')
def logoutuser(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = createuserform()
        if request.method == 'POST':
            form = createuserform(request.POST)
            domain = '@vitap.ac.in'
            regno = request.POST.get('username')
            regemial = request.POST.get('email')
            # if regno in regemial and domain in regemial:
            get_otp = request.POST.get('otp')
            if get_otp:
                get_usr = request.POST.get('usr')
                usr = User.objects.get(username=get_usr)

                if int(get_otp) == Userotp.objects.filter(user=usr).last().otp:
                    usr.is_active = True
                    usr.save()
                    createprofile(request, usr)
                    createauthor(request, usr)

                    messages.success(
                        request, f"Account created sucessfully")
                    return redirect('signin')
                else:
                    messages.error(
                        request, 'You have entered invalid otp')
                    return render(request, 'register.html', {'otp': True, 'usr': usr})
            if form.is_valid():
                if regno in regemial and domain in regemial:
                    form.save()
                    username = form.cleaned_data.get('username')
                    email = form.cleaned_data.get('email')
                    # print(email)
                    usr = User.objects.get(username=username)
                    usr.is_active = False
                    usr.save()
                    usr_otp = random.randint(100000, 999999)
                    Userotp.objects.create(user=usr, otp=usr_otp)
                    mess = f"Hello {usr.username},\n\nYour OTP is {usr_otp}\n\n --Univ`Blog"
                    send_mail("Univ Blog OTP Verification", mess, settings.EMAIL_HOST_USER,
                              [email], fail_silently=False)

                else:
                    messages.warning(
                        request, 'Entered Regno does not match to E-mail')

            return render(request, 'register.html', {'otp': True, 'usr': usr})

    parms = {'form': form}
    return render(request, 'register.html', parms)


def verify(request):
    return render(request, 'verification.html')


def account(request):
    context = {}
    return render(request, 'account.html', context)


def createprofile(request, regno):
    print(regno)
    profile.objects.create(user=regno).save()


def createauthor(request, regno):
    print(regno)
    Author.objects.create(user=regno).save()


def infoprofile(request, id):
    info = User.objects.get(id=id)
    infod = profile.objects.filter(user=info).values()
    authorname = Author.objects.get(user=info)
    userpost = Post.objects.filter(auther=authorname)
    parms = {'infod': infod, 'posts': userpost}
    return render(request, 'profile.html', parms)


# @allowed_users(allowed_roles=[''])
@login_required(login_url='signin')
def editprofile(request, id):
    info = User.objects.get(id=id)
    infod = profile.objects.get(user=info)
    form = modifyprofile(instance=infod)
    if request.method == 'POST':
        form = modifyprofile(request.POST, request.FILES, instance=infod)
        if form.is_valid():
            form.save()
            messages.success(request, f"Profile Updated")

        else:
            messages.ERROR(request, f"Profile Not Updated")
            return redirect('profile')

    parms = {'form': form}
    return render(request, 'edit_profile.html', parms)


# Create your views here.


def pagenotfound(request, exception):
    return render(request, 'pagenotfound.html')
