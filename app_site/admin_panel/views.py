from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import *
from django.db.models import Q
from .models import *
from django.views import generic


def index(request):
    city_list = get_list_or_404(City.objects.order_by('city_name'))
    context = {
        'city_list': city_list,
    }
    return render(request, 'admin_panel/index.html', context)


def city(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    object_list = Object.objects.filter(Q(city__gte=city_id)).order_by('object_name')
    error_message = ""
    if request.method == 'GET':
        search_start = request.GET.get('search_start', None)
        search_end = request.GET.get('search_end', None)
        if search_start == None or search_end == None:
            object_list = Object.objects.filter(Q(city__gte=city_id, available=True)).order_by('object_name')
            error_message = ""
        else:
            if search_start > search_end:
                error_message = "Start date can't be greater than end date!"
            else:
                object_list = Object.objects.filter(
                    Q(city__gte=city_id, available=True, start_date__lte=search_start, end_date__gte=search_end))
                for object in object_list:
                    if Reservation.objects.filter(
                        Q(object=object),
                        Q(start_date__range=(search_start, search_end))
                        | Q(end_date__range=(search_start, search_end))
                        | Q(start_date__lte=search_start, end_date__gte=search_end)
                    ):
                        object_list  = object_list.exclude(pk=object.pk)

    today = str(datetime.date.today())
    context = {
        'error_message': error_message,
        'today': today,
        'city': city,
        'object_list': object_list,
    }
    return render(request, 'admin_panel/city.html', context)


def object(request, city_id, object_id):
    city = get_object_or_404(City, pk=city_id)
    object = get_object_or_404(Object, pk=object_id)
    reservation_list = Reservation.objects.filter(Q(object__gte=object_id)).order_by('start_date')
    error_message = ""

    if request.method == 'GET':
        start = request.GET.get('start', None)
        end = request.GET.get('end', None)
        name = request.GET.get('name', None)

        if start == None or end == None or name == None:
            error_message = "Empty form!"
        else:
            if start > end:
                error_message = "Start date can't be greater than end date!"
            else:
                client = None
                if Client.objects.filter(Q(client_name=name)):
                    client = Client.objects.filter(Q(client_name=name))
                else:
                    c = Client.objects.create(client_name=name)
                    c.save()
                    client = Client.objects.filter(Q(client_name=name))
                client = Client.objects.get(id=client[0].pk)

                print(client)
                r = Reservation.objects.create(client=client, object_id=object_id, start_date=start, end_date=end)
                r.save()

    today = str(datetime.date.today())
    context = {
        'error_message': error_message,
        'today': today,
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
