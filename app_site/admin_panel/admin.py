from django.contrib import admin
from .models import *

admin.site.register(City)
admin.site.register(Reservation)
admin.site.register(Client)


class ObjectReservations(admin.TabularInline):
    model = Reservation
    # TODO Poprawić styl wyświetlania


class ObjectAdmin(admin.ModelAdmin):
    inlines = (ObjectReservations,)

admin.site.register(Object, ObjectAdmin)
