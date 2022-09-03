from django.shortcuts import render, redirect
from .models import Booking, Inventory, Review, Slot, Sport
from Home.models import Profile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

def sports(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
    sports = Sport.objects.all().order_by('name')
    return render(request, 'Sports/sports.html', {'sports': sports})

def sports_filter(request, pk):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
    sports = Sport.objects.filter(name__startswith=pk).order_by('name')
    return render(request, 'Sports/sports.html', {'sports': sports})

def sports_detail(request, sport):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
    sport = Sport.objects.get(name=sport)
    if request.method == 'POST' and request.user.is_authenticated:
        review = request.POST['review']
        user = Profile.objects.get(username=request.user.username)
        Review.objects.create(sport=sport, review=review, user=user)
    inventory = Inventory.objects.filter(sport=sport)
    reviews = Review.objects.filter(sport=sport).order_by('-id')
    return render(request, 'Sports/sports_detail.html', {'sport': sport, 'inventory': inventory, 'reviews': reviews})

def book(request, sport):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
    if not request.user.is_authenticated:
        return redirect('/login?next=' + request.path)
    sport = Sport.objects.get(name=sport)
    profile = Profile.objects.get(username=request.user.username)
    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['slot']
        slot = Slot.objects.get(sport=sport, date=date, time=time)
        if slot.availability == 0:
            return render(request, 'Sports/book.html', {'sport': sport, 'message': 'Sorry, this slot is full. Please select another slot.'})
        user_bookings = Booking.objects.filter(user=profile)
        user_booking_list = []
        for booking in user_bookings:
            if booking.slot.date == slot.date:
                user_booking_list.append(booking.slot.time)
        if len(user_booking_list) >= 3:
            return render(request, 'Sports/book.html', {'sport': sport, 'message': 'You can only book 3 slots per day'})
        subject = 'Booking Confirmation - Mittal Sports Complex'
        message = f'Hi {profile.name},\n\nYour booking for {sport.name} on {slot.date} at {slot.time} has been confirmed.\n\nRegards,\nMittal Sports Complex'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [profile.email]
        try:
            send_mail(subject, message, email_from, recipient_list)
        except:
            pass
        Booking.objects.create(user=profile, sport=sport, slot=slot)
        slot.availability -= 1
        slot.save()
        return redirect('confirmed')
    return render(request, 'Sports/book.html', {'sport': sport})

@api_view(['POST'])
def getSlots(request):
    data = request.data
    date = data.get('date')
    if date < datetime.now().strftime("%Y-%m-%d"):
        return Response({'message': 'Unavailable'}, 403)
    if request.user.is_authenticated:
        if date == datetime.now().strftime("%Y-%m-%d"):
            slots = Slot.objects.filter(date=date, availability__gt=0, time__gte=datetime.now().strftime("%H:%M:%S"))
        else:
            slots = Slot.objects.filter(date=date, availability__gt=0)
        if not slots:
            return Response({'message': 'Unavailable'}, 403)
        s = []
        for slot in slots:
            s.append(slot.time)
        return Response({'slots': s}, 200)
    return Response({'message': 'Unauthorized'}, 401)

@api_view(['POST'])
def getAvailability(request):
    data = request.data
    date = data.get('date')
    time = data.get('time')
    if date < datetime.now().strftime("%Y-%m-%d"):
        return Response({'message': 'Unavailable'}, 403)
    if time < datetime.now().strftime("%H:%M:%S") and date == datetime.now().strftime("%Y-%m-%d"):
        return Response({'message': 'Unavailable'}, 403)
    if request.user.is_authenticated:
        slots = Slot.objects.filter(date=date, time=time)
        if not slots:
            return Response({'message': 'Unavailable'}, 403)
        profile = Profile.objects.get(username=request.user.username)
        a = []
        for slot in slots:
            a.append(slot.availability)
            if Booking.objects.filter(user=profile, slot=slot).exists():
                return Response({'message': 'You have already booked this slot!'}, 402)
        return Response({'availability': a}, 200)
    return Response({'message': 'Unauthorized'}, 401)

def confirmed(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
    try:
        referer = request.META['HTTP_REFERER']
        if not referer.endswith('/book/'):
            return redirect('home')
    except KeyError: return redirect('home')
    return render(request, 'Sports/confirmed.html')