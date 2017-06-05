from django.contrib import admin
from .models import *


class CityAdmin(admin.ModelAdmin):
    search_fields = ('city_name',)
admin.site.register(City, CityAdmin)


class ClientAdmin(admin.ModelAdmin):
    search_fields = ('client_name',)
admin.site.register(Client, ClientAdmin)


def unavailable(modeladmin, request, queryset):
    for object in queryset:
        object.available = False
        object.save()

unavailable.short_description = 'Set as unavailable selected objects'


def available(modeladmin, request, queryset):
    for object in queryset:
        object.available = True
        object.save()

available.short_description = 'Set as available selected objects'


class ObjectReservations(admin.TabularInline):
    model = Reservation
    extra = 1


class ObjectAdmin(admin.ModelAdmin):
    inlines = (ObjectReservations,)
    actions = [unavailable, available]
    list_display = ('object_name', 'city', 'start_date', 'end_date', 'available',)
    list_filter = ('available', 'city', 'start_date', 'end_date',)
    search_fields = ('object_name',)

admin.site.register(Object, ObjectAdmin)
admin.site.register(Reservation)
