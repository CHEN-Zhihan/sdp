from django.conf.urls import url


from django.contrib.auth import views as authViews
from .forms import LoginForm
from .views import participant,instructor,authenticate,administrator

participantURL = r'^participant/(?P<participantID>[0-9]+)'
instructorURL = r'^instructor/(?P<instructorID>[0-9]+)'
courseURL = instructorURL+r'/(?P<courseID>[0-9]+)'
moduleURL = courseURL + r'/(?P<moduleID>[0-9]+)'
administratorURL=r'^administrator/(?P<administratorID>[0-9]+)'

urlpatterns = [
    url(participantURL+r'$',participant.participantIndex,name="participantIndex"),
    url(participantURL+r'/showCourseList$',participant.showCourseList,name="showCourseList"),
    url(participantURL+r'/showCourse$',participant.showCourse,name="showCourse"),
    url(participantURL+r'/enroll$',participant.enroll,name="enroll"),
    url(instructorURL+r'$',instructor.instructorIndex,name="instructorIndex"),
    url(instructorURL+r'/newCourse$',instructor.newCourse,name="newCourse"),
    url(courseURL+r'$',instructor.coursePage,name="coursePage"),
    url(courseURL+r'/newModule$',instructor.newModule,name="newModule"),
    url(moduleURL+r'$',instructor.modulePage,name="modulePage"),
    url(moduleURL+r'/newComponent$',instructor.newComponent,name="newComponent"),
    url(administratorURL+r'$',administrator.administratorIndex,name="administratorIndex"),
    url('login/$',authenticate.myLogin,name="myLogin"),
    url('logout/$',authenticate.myLogout,name="myLogout"),
    url('register/$',authenticate.register,name="register"),
]
