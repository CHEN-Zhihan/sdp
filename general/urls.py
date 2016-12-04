from django.conf.urls import url
from .views import participant, instructor, authenticate, administratorHR

participantURL = r'^Participant/(?P<participantID>[0-9]+)'
instructorURL = r'^Instructor/(?P<instructorID>[0-9]+)'
participantCourseURL = participantURL+r'/(?P<courseID>[0-9]+)'
instructorCourseURL = instructorURL+r'/(?P<courseID>[0-9]+)'
instructorModuleURL = instructorCourseURL + r'/(?P<moduleIndex>[0-9]+)'
participantModuleURL = participantCourseURL + r'/(?P<moduleIndex>[0-9]+)'
administratorURL = r'^Administrator/(?P<administratorID>[0-9]+)'

urlpatterns = [
    url(participantURL+r'$', participant.ParticipantIndex, name="ParticipantIndex"),
    url(participantURL+r'/showCourseList$', participant.showCourseList, name="showCourseList"),
    url(participantCourseURL+r'$', participant.viewCourse, name="viewCourse"),
    url(participantModuleURL+r'$', participant.viewModule, name="viewModule"),
    url(instructorURL+r'$', instructor.InstructorIndex, name="InstructorIndex"),
    url(instructorURL+r'/newCourse$', instructor.newCourse, name="newCourse"),
    url(instructorCourseURL+r'$', instructor.coursePage, name="coursePage"),
    url(instructorCourseURL+r'/changeModuleOrder$', instructor.changeModuleOrder, name="changeModuleOrder"),
    url(instructorCourseURL+r'/newModule$', instructor.newModule, name="newModule"),
    url(instructorCourseURL+r'/editCourse$', instructor.editCourse, name="editCourse"),
    url(instructorModuleURL+r'$', instructor.modulePage, name="modulePage"),
    url(instructorModuleURL+r'/editModule$', instructor.editModule, name="editModule"),
    url(instructorModuleURL+r'/changeComponentOrder$', instructor.changeComponentOrder, name="changeComponentOrder"),
    url(instructorModuleURL+r'/newComponent$', instructor.newComponent, name="newComponent"),
    url(administratorURL+r'$', administratorHR.AdministratorIndex, name="AdministratorIndex"),
    url(r'^HR/(?P<HRID>[0-9]+)$', administratorHR.HRIndex, name="HRIndex"),
    url(r'login/$', authenticate.myLogin, name="myLogin"),
    url(r'^$', authenticate.myLogin, name="homeLogin"),
    url(r'logout/$', authenticate.myLogout, name="myLogout"),
]
