from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile
from Sports.models import Booking, Sport
import random
from django.core.mail import send_mail
from django.conf import settings
from threading import Thread
import datetime
from django.db.models import Count

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
    trending = Sport.objects.all().annotate(num=Count('booking')).order_by('-num')[:3]
    return render(request, 'Home/home.html', locals())

def login(request):
    if request.user.is_authenticated: return redirect('home')
    redirect_to = request.GET['next'] if 'next' in request.GET else 'home'
    if request.method == 'POST':
        param = request.POST['param']
        password = request.POST['password']
        if '@' in param:
            if User.objects.filter(email=param).exists():
                user = User.objects.get(email=param)
                if user.is_staff:
                    user = auth.authenticate(username=user.username, password=password)
                    if not user:
                        return render(request, 'Home/login.html', {'message': 'Invalid Password', 'redirect_to': redirect_to})
                    auth.login(request, user)
                    return redirect('/admin')
                profile = Profile.objects.get(email=param)
                if not profile.email_verified:
                    profile.delete()
                    user.delete()
                    return render(request, 'Home/login.html', {'message': 'User not found', 'redirect_to': redirect_to})
                user = auth.authenticate(username=user.username, password=password)
                if not user:
                    return render(request, 'Home/login.html', {'message': 'Invalid Password', 'redirect_to': redirect_to})
                auth.login(request, user)
                return redirect(request.GET['next'] if 'next' in request.GET else 'home')
            else:
                return render(request, 'Home/login.html', {'message': 'User not found', 'redirect_to': redirect_to})
        else:
            if User.objects.filter(username=param).exists():
                user = User.objects.get(username=param)
                if user.is_staff:
                    user = auth.authenticate(username=user.username, password=password)
                    if not user:
                        return render(request, 'Home/login.html', {'message': 'Invalid Password', 'redirect_to': redirect_to})
                    auth.login(request, user)
                    return redirect('/admin')
                profile = Profile.objects.get(username=param)
                if not profile.email_verified:
                    profile.delete()
                    user.delete()
                    return render(request, 'Home/login.html', {'message': 'User not found', 'redirect_to': redirect_to})
                user = auth.authenticate(username=user.username, password=password)
                if not user:
                    return render(request, 'Home/login.html', {'message': 'Invalid Password', 'redirect_to': redirect_to})
                auth.login(request, user)
                return redirect(request.GET['next'] if 'next' in request.GET else 'home')
            else:
                return render(request, 'Home/login.html', {'message': 'User not found', 'redirect_to': redirect_to})
    return render(request, 'Home/login.html', locals())

def signup(request):
    if request.user.is_authenticated: return redirect('home')
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        # if len(password) < 8:
        #     return render(request, 'Home/signup.html', {'message': 'Password must be at least 8 characters long'})
        for i in username:
            if i not in 'abcdefghijklmnopqrstuvwxyz0123456789._':
                return render(request, 'Home/signup.html', {'message': 'Username can only contain alphabets, numbers, periods and underscores'})
        if User.objects.filter(username=username).exists():
            profile = Profile.objects.get(username=username)
            if not profile.email_verified:
                user = User.objects.get(username=username)
                user.delete()
                profile.delete()
                dataset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                otp = ''.join(random.choice(dataset) for _ in range(8))
                if Profile.objects.filter(otp=otp).exists():
                    otp = ''.join(random.choice(dataset) for _ in range(8))
                subject = f'Email Verification - {settings.SITE_NAME}'
                message = f'Hello {name},\n\nThank you for signing up with {settings.SITE_NAME}.\n\nYour OTP is {otp}.\n\nPlease enter this OTP to verify your email.\n\nThank you,\n{settings.SITE_NAME}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email,]
                try:
                    Thread(target=send_mail(subject, message, email_from, recipient_list)).start()
                except:
                    return render(request, 'Home/signup.html', {'message': 'Error sending OTP'})
                Profile.objects.create(name=name, username=username, email=email, otp=otp)
                User.objects.create_user(username=username, password=password, email=email)
                return redirect('signup_otp')
            return render(request, 'Home/signup.html', {'message': 'Username is already taken'})
        if User.objects.filter(email=email).exists():
            profile = Profile.object.get(email=email)
            if not profile.email_verified:
                user = User.objects.get(email=email)
                user.delete()
                profile.delete()
                dataset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                otp = ''.join(random.choice(dataset) for _ in range(8))
                if Profile.objects.filter(otp=otp).exists():
                    otp = ''.join(random.choice(dataset) for _ in range(8))
                subject = f'Email Verification - {settings.SITE_NAME}'
                message = f'Hello {name},\n\nThank you for signing up with {settings.SITE_NAME}.\n\nYour OTP is {otp}.\n\nPlease enter this OTP to verify your email.\n\nThank you,\n{settings.SITE_NAME}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email,]
                try:
                    Thread(target=send_mail(subject, message, email_from, recipient_list)).start()
                except:
                    return render(request, 'Home/signup.html', {'message': 'Error sending OTP'})
                Profile.objects.create(name=name, username=username, email=email, otp=otp)
                User.objects.create_user(username=username, password=password, email=email)
                return redirect('signup_otp')
            return render(request, 'Home/signup.html', {'message': 'Email is already registered'})
        dataset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        otp = ''.join(random.choice(dataset) for _ in range(8))
        if Profile.objects.filter(otp=otp).exists():
            otp = ''.join(random.choice(dataset) for _ in range(8))
        subject = f'Email Verification - {settings.SITE_NAME}'
        message = f'Hello {name},\n\nThank you for signing up with {settings.SITE_NAME}.\n\nYour OTP is {otp}.\n\nPlease enter this OTP to verify your email.\n\nThank you,\n{settings.SITE_NAME}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        try:
            send_mail(subject, message, email_from, recipient_list)
        except:
            return render(request, 'Home/signup.html', {'message': 'Error sending OTP'})
        Profile.objects.create(name=name, username=username, email=email, otp=otp)
        User.objects.create_user(username=username, password=password, email=email)
        return redirect('signup_otp')
    return render(request, 'Home/signup.html')

def signup_otp(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
    try:
        referer = request.META['HTTP_REFERER']
        if not (referer.endswith('/signup/') or referer.endswith('/signup/verify/')):
            return redirect('home')
    except KeyError: return redirect('home')
    if request.user.is_authenticated: return redirect('home')
    if request.method == 'POST':
        otp = request.POST['otp']
        if Profile.objects.filter(otp=otp).exists():          # I know this is highly unsecure, but it's a temporary solution
            profile = Profile.objects.get(otp=otp)
            profile.otp = '0'
            profile.email_verified = True
            profile.save()
            return redirect('login')
        else:
            return render(request, 'Home/signup_otp.html', {'message': 'Invalid OTP'})
    return render(request, 'Home/signup_otp.html')

def reset(request):
    if request.user.is_authenticated: return redirect('home')
    if request.method == 'POST':
        param = request.POST['param']
        if '@' in param:
            if User.objects.filter(email=param).exists():
                user = User.objects.get(email=param)
                profile = Profile.objects.get(email=param)
                if not profile.email_verified:
                    profile.delete()
                    user.delete()
                    return render(request, 'Home/reset.html', {'message': 'User not found'})
                dataset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                otp = ''.join(random.choice(dataset) for _ in range(8))
                if Profile.objects.filter(otp=otp).exists():
                    otp = ''.join(random.choice(dataset) for _ in range(8))
                profile.otp = otp
                profile.save()
                subject = f'Password Reset - {settings.SITE_NAME}'
                message = f'Hello {profile.name},\n\nYou have requested to reset your password.\n\nYour OTP is {otp}.\n\nPlease enter this OTP to reset your password.\n\nThank you,\n{settings.SITE_NAME}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [param,]
                try:
                    send_mail(subject, message, email_from, recipient_list)
                except:
                    return render(request, 'Home/reset.html', {'message': 'Error sending OTP'})
                return redirect('reset_otp')
            else:
                return render(request, 'Home/reset.html', {'message': 'User not found'})
        else:
            if User.objects.filter(username=param).exists():
                user = User.objects.get(username=param)
                profile = Profile.objects.get(username=param)
                if not profile.email_verified:
                    profile.delete()
                    user.delete()
                    return render(request, 'Home/login.html', {'message': 'User not found'})
                dataset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                otp = ''.join(random.choice(dataset) for _ in range(8))
                if Profile.objects.filter(otp=otp).exists():
                    otp = ''.join(random.choice(dataset) for _ in range(8))
                profile.otp = otp
                profile.save()
                subject = f'Password Reset - {settings.SITE_NAME}'
                message = f'Hello {profile.name},\n\nYou have requested to reset your password.\n\nYour OTP is {otp}.\n\nPlease enter this OTP to reset your password.\n\nThank you,\n{settings.SITE_NAME}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email,]
                try:
                    send_mail(subject, message, email_from, recipient_list)
                except:
                    return render(request, 'Home/reset.html', {'message': 'Error sending OTP'})
                return redirect('reset_otp')
            else:
                return render(request, 'Home/reset.html', {'message': 'User not found'})
    return render(request, 'Home/reset.html')

def reset_otp(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
    try:
        referer = request.META['HTTP_REFERER']
        if not (referer.endswith('/forgot/') or referer.endswith('/forgot/verify/')):
            return redirect('home')
    except KeyError: return redirect('home')
    if request.user.is_authenticated: return redirect('home')
    if request.method == 'POST':
        otp = request.POST['otp']
        if Profile.objects.filter(otp=otp).exists():
            profile = Profile.objects.get(otp=otp)
            profile.otp = '0'
            profile.save()
            return redirect(f'/forgot/reset/{profile.username}/')
        else:
            return render(request, 'Home/reset_otp.html', {'message': 'Invalid OTP'})
    return render(request, 'Home/reset_otp.html')

def reset_password(request, username):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
    try:
        referer = request.META['HTTP_REFERER']
        if not (referer.endswith('/forgot/verify/') or referer.endswith(f'/forgot/reset/{username}/')):
            return redirect('home')
    except KeyError: return redirect('home')
    if request.user.is_authenticated: return redirect('home')
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if len(password) < 8:
            return render(request, 'Home/reset_password.html', {'message': 'Password must be at least 8 characters long', 'username': username})
        if password == confirm_password:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            return render(request, 'Home/reset_password.html', {'message': 'Passwords do not match', 'username': username})
    return render(request, 'Home/reset_password.html', {'username': username})

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('home')

def bookings(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
    past = []
    upcoming = []
    if request.user.is_authenticated:
        profile = Profile.objects.get(username=request.user.username)
        bookings = Booking.objects.filter(user=profile)
        for booking in bookings:
            if booking.slot.date < datetime.date.today():
                past.append(booking)
            elif booking.slot.date == datetime.date.today() and booking.slot.time < datetime.datetime.now().time():
                past.append(booking)
            else:
                upcoming.append(booking)
    return render(request, 'Home/bookings.html', {'past': past, 'upcoming': upcoming})