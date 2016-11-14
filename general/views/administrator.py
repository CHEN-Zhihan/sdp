from . import authenticate
from ..models import Participant,Administrator,Instructor,HR
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect

@login_required
def AdministratorIndex(request,administratorID):
    if "Administrator" not in list(map((lambda x:x.name),request.user.groups.all())):
        return redirect("myLogout")
    if request.method=="POST":
        username = request.POST.get("username")
        newInstructor=Administrator.designate(username,Instructor)
        return redirect('administratorIndex',administratorID)
    else:
        participantList = set(map((lambda x:x._user.username),Participant.objects.all()))
        instructorList = set(map((lambda x:x._user.username),Instructor.objects.all()))
        return render(request,"general/administratorIndex.html",{"usernameList":participantList-instructorList})