from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.mail import send_mail

import calendar
import datetime
import time

from snolab_booking.models import Apartment, Bed, Booking, Visit
from snolab_booking.forms import VisitForm

def prev_date(year, month):
    """ Return tuple of previous year & month for 1 month back."""
    if month == 1:
        return [year - 1, 12]
    else:
        return [year, month - 1]

def next_date(year, month):
    """ Return tuple of previous year & month for 1 month forward."""
    if month == 12:
        return [year + 1, 1]
    else:
        return [year, month + 1]


def bookings_per_month(year, month):
    """ Bookings per day for the month."""
    day_information = []
    year, month = int(year), int(month)
    cal = calendar.Calendar(6) # Weeks start on Sunday    
    for day in cal.itermonthdays(year, month):
        if day == 0: # Days not in month are 0 (yields full week)
            day_information.append([day,None])
            continue
        # Include bookings with a check in before or on today and exclude with a check out before today
        bookings = Booking.objects.filter(check_in__lte=datetime.datetime(year, month, day))
        bookings = bookings.exclude(check_out__lt=datetime.datetime(year, month, day))
        day_information.append([day, bookings])
    return day_information                    

def bookings(request, year, month):
    """ View of bookings in a month."""
    year = int(year)
    month = int(month)
    return render(request, 'snolab_booking/bookings.html', {'day_bookings' : bookings_per_month(year, month),
                                                            'now' : [year, month],
                                                            'prev' : prev_date(year, month),
                                                            'next' : next_date(year, month)})

def visits_per_month(year, month):
    """ Vists per day for the month."""
    day_information = []
    year, month = int(year), int(month)
    cal = calendar.Calendar(6) # Weeks start on Sunday    
    for day in cal.itermonthdays(year, month):
        if day == 0: # Days not in month are 0 (yields full week)
            day_information.append([day,None])
            continue
        # Include bookings with a check in before or on today and exclude with a check out before today
        visits = Visit.objects.filter(check_in__lte=datetime.datetime(year, month, day))
        visits = visits.exclude(check_out__lt=datetime.datetime(year, month, day))
        day_information.append([day, visits])
    return day_information

def visits(request, year, month):
    """ View of visits in a month."""
    year = int(year)
    month = int(month)
    return render(request, 'snolab_booking/visits.html', {'day_visits' : visits_per_month(year, month),
                                                          'now' : [year, month],
                                                          'prev' : prev_date(year, month),
                                                          'next' : next_date(year, month)})

def index(request):
    """ View of visits and bookings in this month."""
    year, month = time.localtime()[:2]
    return render(request, 'snolab_booking/index.html', {'day_visits' : visits_per_month(year, month),
                                                         'day_bookings' : bookings_per_month(year, month),
                                                         'now' : [year, month],
                                                         'prev' : prev_date(year, month),
                                                         'next' : next_date(year, month)})

class Apartments(generic.ListView):
    model = Apartment
    template_name = "snolab_booking/apartments.html"

def apartment(request, apartment_id):
    """ Return apartment information."""
    apartment = get_object_or_404(Apartment, pk=apartment_id)
    try:
        beds = Bed.objects.filter(apartment=apartment_id)
        return render(request, 'snolab_booking/apartment.html', {'apartment' : apartment, 'bed_list' : beds})
    except Bed.DoesNotExist:
        return render(request, 'snolab_booking/apartment.html', {'apartment' : apartment, 'bed_list' : []})

def booking(request, booking_id):
    """ List a booking."""
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'snolab_booking/booking.html', {'booking' : booking})

def visit(request, visit_id):
    """ List a visit."""
    visit = get_object_or_404(Visit, pk=visit_id)
    return render(request, 'snolab_booking/visit.html', {'visit' : visit})

def visit_booking(request):
    """ Book visit form."""
    if request.method == 'POST': 
        form = VisitForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            clean_data = form.cleaned_data
            print clean_data
            visit = Visit(contact=clean_data['contact'], 
                          check_in=clean_data['check_in'],
                          check_out=clean_data['check_out'],
                          experiment=clean_data['experiment'])
            visit.save()
#            send_mail("Room Request", clean_data['contact']
#                cd['subject'],
#                cd['message'],
#                cd.get('email', 'noreply@example.com'),
#                ['siteowner@example.com'],
#                )
            return render(request, 'snolab_booking/visit_booking.html') # Redirect after POST
    else:
        form = VisitForm() # An unbound form
    return render(request, 'snolab_booking/visit_booking.html', {'form': form})
