from django.conf.urls import url

from . import views

app_name = 'admin_panel'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<city_id>[0-9]+)/$', views.city, name='city'),
    url(r'^(?P<city_id>[0-9]+)/(?P<object_id>[0-9]+)/$', views.object, name='object'),
    url(r'^(?P<city_id>[0-9]+)/(?P<object_id>[0-9]+)/(?P<reservation_id>[0-9]+)/$', views.reservation, name='reservation'),
]
