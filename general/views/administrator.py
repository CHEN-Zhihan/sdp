from . import authenticate
from ..userModels import Participant,Administrator,Instructor,HR,SDPUser
from ..courseModels import Course
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect

@login_required
def AdministratorIndex(request,administratorID):
    administratorID=int(administratorID)
    if not authenticate.roleCheck(request.user,"Administrator",administratorID):
        return redirect("myLogout")
    admin=Administrator.getFromUser(request.user)
    if request.method=="POST":
        username = request.POST.get("username")
        user=User.objects.get(username=username)
        newInstructor=Administrator.designate(user,"Instructor")
        return redirect('AdministratorIndex',administratorID)
    else:
        allUserList = set(map((lambda x:x.username),User.objects.all()))
        instructorList = set(map((lambda x:x.getUser().username),Instructor.objects.all()))
        courses = Course.objects.all()
        for course in courses:
            print(course.instructor)
        return render(request,"general/administratorIndex.html",{"users":allUserList-instructorList,"courses":courses})
