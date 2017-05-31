from django.db import models
from django.db.models import Q
from django.db import IntegrityError
import datetime


class City(models.Model):
    city_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.city_name


class Client(models.Model):
    client_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.client_name


class Object(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    object_name = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    start_date = models.DateField('Occupied from', default=datetime.date.today)
    end_date = models.DateField('Occupied to', default=datetime.date.today)
    reservations = models.ManyToManyField(Client, through='Reservation')

    def __str__(self):
        return '%s - %s' % (self.city, self.object_name)


class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    start_date = models.DateField('Occupied from', default=datetime.date.today)
    end_date = models.DateField('Occupied to', default=datetime.date.today)

    def __str__(self):
        return '%s - %s' % (self.start_date, self.end_date)
    def save(self, *args, **kwargs):
        if Reservation.objects.filter(Q(object=self.object), Q(object__available=False)):
            raise IntegrityError("Object is not available!")
        elif Reservation.objects.filter(
            Q(object=self.object),
            Q(start_date__range=(self.start_date, self.end_date))
            | Q(end_date__range=(self.start_date, self.end_date))
            | Q(start_date__lte=self.start_date, end_date__gte=self.end_date)
        ):
            raise IntegrityError("Object booked for this term!")
        # TODO Poprawić warunek
        elif Reservation.objects.filter(
            Q(object=self.object),
            ~Q(object__start_date__range=(self.start_date, self.end_date))
            | ~Q(object__end_date__range=(self.start_date, self.end_date))
            | Q(object__start_date__lte=self.start_date, object__end_date__gte=self.end_date)
        ):
            raise IntegrityError("Object is not available for this term!")
        else:
            super(Reservation, self).save(*args, **kwargs)
