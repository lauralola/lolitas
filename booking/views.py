from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import *
from django.contrib import messages

def index(request):
    return render(request, 'index.html',{})

def menu(request):
    return render(request, 'menu.html',{})

def booking(request):
    weekdays = validWeekday(22)

    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == 'POST':
        table = request.POST.get('table')
        day = request.POST.get('day')
        if table == None:
            messages.success(request, 'Please select a Table')
            return redirect('booking')

        request.session['day'] = day
        request.session['table'] = table

        return redirect('bookingSubmit')

    return render(request, 'booking.html', {
        'weekdays': weekdays,
        'validateWeekdays': validateWeekdays,
    })

def bookingSubmit(request):
    user = request.user
    times = [
        '6PM', '9PM'
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate= strdeltatime

    day = request.session.get('day')
    table = request.session.get('table')

    hour = checkTime(times, day)
    if request.method == 'POST':
        time = request.POST.get('time')
        date = dayToWeekday(day)

        if table != None:
            if day <= maxDate and day >= minDate:
                if date == "Friday" or date == "Saturday":
                    if Booking.objects.filter(day=day).count() <11:
                        if Booking.objects.filter(day=day, time=time).count() <1:
                            BookingForm = Booking.objects.get_or_create(
                                user = user,
                                table = table,
                                day = day,
                                time = time,
                            )
                            messages.success(request, 'Booking Made!')
                            return redirect('index')
                        else:
                            messages.success(request, 'The Selected Table has been Reserved!')
                    else:
                        messages.success(request, 'The Selected Date is Full'),
                else: 
                    messages.success(request, 'The Selected Date is Incorrect')
            else:
                messages.success(request, 'The Selected Time is Incorrect')
        else:
            messages.success(request, "Please select a Table")

                
    return render(request, 'bookingSubmit.html', {
            'times':hour,
        })

def userPanel(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).order_by('day', 'time')
    return render(request, 'userPanel.html', {
        'user':user,
        'bookings':bookings,
    })

def userUpdate(request, id):
    booking = Booking.objects.get(pk=id)
    userdatepicked = appointment.day
    #Copy  booking:
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')

    #24h if statement in template:
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    

    if request.method == 'POST':
        service = request.POST.get('table')
        day = request.POST.get('day')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['table'] = table

        return redirect('userUpdateSubmit', id=id)


    return render(request, 'userUpdate.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
            'delta24': delta24,
            'id': id,
        })

def userUpdateSubmit(request, id):
    user = request.user
    times = [
        "6 PM", "9 PM",
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    table = request.session.get('table')
    
    #Only show the time of the day that has not been selected before and the time he is editing:
    hour = checkEditTime(times, day, id)
    booking = Booking.objects.get(pk=id)
    userSelectedTime = booking.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
            if day <= maxDate and day >= minDate:
                if date == 'Friday' or date == 'Saturday':
                    if Booking.objects.filter(day=day).count() < 11:
                        if Booking.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                            BookingForm = Booking.objects.filter(pk=id).update(
                                user = user,
                                table = table,
                                day = day,
                                time = time,
                            ) 
                            messages.success(request, "Appointment Edited!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")
        return redirect('userPanel')


    return render(request, 'userUpdateSubmit.html', {
        'times':hour,
        'id': id,
    })

def staffPanel(request):
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime
    #Only show the Appointments 21 days from today
    items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

    return render(request, 'staffPanel.html', {
        'items':items,
    })

def dayToWeekday(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y

def validWeekday(days):
    #Loop days you want in the next 21 days:
    today = datetime.now()
    weekdays = []
    for i in range (0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y == 'Monday' or y == 'Saturday' or y == 'Wednesday':
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays
    
def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays

def checkTime(times, day):
    #Only show the time of the day that has not been selected before:
    x = []
    for k in times:
        if Booking.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x

def checkEditTime(times, day, id):
    #Only show the time of the day that has not been selected before:
    x = []
    booking = Booking.objects.get(pk=id)
    time = booking.time
    for k in times:
        if Booking.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x
    
