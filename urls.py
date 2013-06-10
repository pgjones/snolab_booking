from django.conf.urls import patterns, url

from snolab_booking import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^booking/(?P<booking_id>\d+)/$', views.booking, name='booking'),
                       url(r'^bookings/(?P<year>\d+)/(?P<month>\d+)/$', views.bookings, name='bookings'),
                       url(r'^visit/(?P<visit_id>\d+)/$', views.visit, name='visit'),
                       url(r'^visit/booking/$', views.visit_booking, name='visit_booking'),
                       url(r'^visits/(?P<year>\d+)/(?P<month>\d+)/$', views.visits, name='visits'),
                       url(r'^apartments/$', views.Apartments.as_view(), name='apartments'),
                       url(r'^apartment/(?P<apartment_id>\d+)/$', views.apartment, name='apartment'),
)
