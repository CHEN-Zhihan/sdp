from django.conf.urls import url

from . import views
from django.contrib.auth import views as authViews
from .forms import LoginForm

participant = r'^participant/(?P<participantID>[0-9]+)'
instructor = r'^instructor/(?P<instructorID>[0-9]+)'
course = instructor+r'/(?P<courseID>[0-9]+)'
module = course + r'/(?P<moduleID>[0-9]+)'

urlpatterns = [
    url(participant+r'$',views.participantIndex,name="participantIndex"),
    url(participant+r'/showCourseList$',views.showCourseList,name="showCourseList"),
    url(participant+r'/showCourse$',views.showCourse,name="showCourse"),
    url(participant+r'/enroll$',views.enroll,name="enroll"),
    url(instructor,views.instructorIndex,name="instructorIndex"),
    url(instructor+r'/newCourse$',views.newCourse,name="newCourse"),
    url(course+r'$',views.coursePage,name="coursePage"),
    url(course+r'/newModule$',views.newModule,name="newModule"),
    url(module+r'$',views.modulePage,name="modulePage"),
    url(module+r'/newComponent$',views.newComponent,name="newComponent"),
]
