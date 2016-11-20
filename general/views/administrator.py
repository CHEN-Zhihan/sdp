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
        users = list(map(UserAdapter,User.objects.all()))
        users.sort(key=(lambda x:x.username))
        courses = Course.objects.all()
        return render(request,"general/administratorIndex.html",{"users":users,"courses":courses})


class UserAdapter():
    def __init__(self,user):
        self.username=user.username
        self.name="{} {}".format(user.first_name,user.last_name)
        self.groups=list(map((lambda x:x.name),user.groups.all()))
        if "Instructor" not in self.groups:
            self.isInstructor=False
        else:
            self.isInstructor=True