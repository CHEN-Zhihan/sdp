from django.conf.urls import url

from . import views
from django.contrib.auth import views as authViews
from .forms import LoginForm

urlpatterns = [
    url(r'^$',views.index,name="index"),
    url(r'^participant/(?P<participantID>[0-9]+)/$',views.participant,name='participant'),
    url(r'^participant/(?P<participantID>[0-9]+)/courses/(?P<courseID>[0-9]+)$',views.courses,name='courses'),
    url(r'^participant/(?P<participantID>[0-9]+)/courses/(?P<courseID>[0-9]+)/enroll$',views.enrollIn,name='enroll'),
    url(r'^instructor/(?P<instructorID>[0-9]+)/$',views.instructor,name='instructor'),
    url(r'^instructor/(?P<instructorID>[0-9]+)/developingCourse/(?P<courseID>[0-9]+)$',views.developingCourse,name='developingCourse'),
    url(r'^instructor/(?P<instructorID>[0-9]+)/new/$',views.newCourse,name='newCourse'),
    url(r'^instructor/(?P<instructorID>[0-9]+)/courses/(?P<courseID>[0-9]+)/newModule/',views.newModule,name='newModule'),
    url(r'getCatalog$',views.showCatalog, name="showCatalog"),
]
