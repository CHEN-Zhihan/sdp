from . import authenticate
from ..models import Participant,Administrator,Instructor,HR,SDPUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect

@login_required
def AdministratorIndex(request,administratorID):
    if "Administrator" not in list(map((lambda x:x.name),request.user.groups.all())):
        print("Not an administrator")
        return redirect("myLogout")
    admin=Administrator.getFromUser(request.user)
    if admin.id!=int(administratorID):
        print("Invalid administratorID")
        return redirect("AdministratorIndex",admin.id)
    if request.method=="POST":
        username = request.POST.get("username")
        user=User.objects.get(username=username)
        newInstructor=Administrator.designate(user,"Instructor")
        return redirect('AdministratorIndex',administratorID)
    else:
        allUserList = set(map((lambda x:x.username),User.objects.all()))
        instructorList = set(map((lambda x:x.getUser().username),Instructor.objects.all()))
        return render(request,"general/administratorIndex.html",{"usernameList":allUserList-instructorList})