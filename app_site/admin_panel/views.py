from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import *
from django.db.models import Q
from .models import *


def index(request):
    city_list = get_list_or_404(City.objects.order_by('city_name'))
    context = {
        'city_list': city_list,
    }
    return render(request, 'admin_panel/index.html', context)


def city(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    object_list = Object.objects.filter(Q(city__gte=city_id)).order_by('object_name')
    context = {
        'city': city,
        'object_list': object_list,
    }
    return render(request, 'admin_panel/city.html', context)


"""
def client(request, client_id):
    return HttpResponse("You're looking at city %s." % client_id)
"""


def object(request, city_id, object_id):
    city = get_object_or_404(City, pk=city_id)
    object = get_object_or_404(Object, pk=object_id)
    reservation_list = Reservation.objects.filter(Q(object__gte=object_id)).order_by('start_date')
    context = {
        'city': city,
        'object': object,
        'reservation_list': reservation_list,
    }
    return render(request, 'admin_panel/object.html', context)


def reservation(request, city_id, object_id, reservation_id):
    city = get_object_or_404(City, pk=city_id)
    object = get_object_or_404(Object, pk=object_id)
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    context = {
        'city': city,
        'object': object,
        'reservation': reservation,
    }
    return render(request, 'admin_panel/reservation.html', context)
