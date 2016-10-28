from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.index,name="index"),
    url(r'getCatalog$',views.showCatalog, name="gg"),
    url(r'^(?P<participantID>[0-9]+)/$',views.participant,name='participant'),
    url(r'^(?P<participantID>[0-9]+)/courses/(?P<courseID>[0-9]+)$',views.courses,name='courses'),
]
