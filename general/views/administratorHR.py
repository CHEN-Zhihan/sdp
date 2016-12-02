from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from ..userModels import Administrator, Instructor, HR
from ..userModels import UserManager
from ..courseModels import Course


@login_required
def AdministratorIndex(request, administratorID):
    administratorID = int(administratorID)
    admin = UserManager.getInstance().getFromUser(request.user, Administrator, administratorID)
    if admin is not None:
        if request.method == "POST":
            try:
                username = request.POST.get("username")
                user = User.objects.get(username=username)
                _ = admin.designate(user, Instructor)
            except Exception as err:
                result = False
                print(err)
            else:
                result = True
            return JsonResponse({"result": result})
        else:
            users = list(map(UserAdapter, User.objects.all()))
            users.sort(key=(lambda x: x.username))
            courses = Course.getAllCourses()
            return render(request, "general/administratorIndex.html", {"users": users,
                                                                       "courses": courses})
    return redirect("myLogout")


@login_required
def HRIndex(request, HRID):
    HRID = int(HRID)
    hr = UserManager.getInstance().getFromUser(request.user, HR, HRID)
    if hr is not None:
        users = list(map(UserAdapter, User.objects.all()))
        users.sort(key=(lambda x: x.username))
        return render(request, "general/HRIndex.html", {"users": users})
    return redirect("myLogout")


class UserAdapter():
    def __init__(self, user):
        self.username = user.username
        self.name = "{} {}".format(user.first_name, user.last_name)
        self.groups = list(map((lambda x: x.name), user.groups.all()))
        if "Instructor" not in self.groups:
            self.isInstructor = False
        else:
            self.isInstructor = True
