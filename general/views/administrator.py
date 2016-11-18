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
    admin=SDPUser.getFromUser(request.user,"Administrator")
    if admin.id!=administratorID:
        print("Invalid administratorID")
        return redirect("AdministratorIndex",admin.id)
    if request.method=="POST":
        username = request.POST.get("username")
        newInstructor=Administrator.designate(username,"Instructor")
        return redirect('administratorIndex',administratorID)
    else:
        allUserList = set(map((lambda x:x.name),User.objects.all()))
        instructorList = set(map((lambda x:x.getUser().username),Instructor.objects.all()))
        return render(request,"general/administratorIndex.html",{"usernameList":allUserList-instructorList})