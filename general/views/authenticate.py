from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from ..userModels import Participant, Instructor, HR, Administrator, UserManager
from ..courseModels import Category

lookup = {"Instructor": Instructor, "HR": HR, "Administrator": Administrator, "Participant": Participant}


def myLogin(request):
    initialize()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        userManager = UserManager.getInstance()
        if request.POST.get('action') == 'LOGIN':
            usertype = request.POST.get('usertype')
            user = authenticate(username=username, password=password)
            if user is not None and userManager.userInGroup(user, lookup[usertype]):
                login(request, user)
                uid = userManager.getUserGroupID(user, lookup[usertype])
                return JsonResponse({
                    "result": True,
                    "url": usertype + "/" + str(uid)
                })
            else:
                return JsonResponse({"result": False})
        elif request.POST.get('action') == 'REGISTER':
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            if not isValidUsername(username):
                return JsonResponse({"result": False, "errno": -2})
            elif User.objects.filter(username=username).exists():
                return JsonResponse({"result": False, "errno": -1})
            else:
                newUser = userManager.createWithNewUser(username, password, firstName, lastName, Participant)
                login(request, newUser.getUser())
                return JsonResponse({
                    "result": True,
                    "url": "Participant/" + str(newUser.id)
                })
    else:
        return render(request, "general/login.html")


def myLogout(request):
    logout(request)
    return redirect('myLogin')


def isValidChar(char):
    return char.isalnum() or char == '-' or char == '_'


def isValidUsername(username):
    if len(username) == 8:
        return all(map(isValidChar, username))
    return False


def initialize():
    categoryList = ["Mergers and Acquisitions", "Markets", "Risk Management", "Securities",
                    "Financial Modelling", "Operations", "Information Technology"]
    for name in categoryList:
        if not Category.objects.filter(name=name).exists():
            category = Category()
            category.name = name
            category.save()
    roleList = ["Instructor", "Participant", "HR", "Administrator"]
    for role in roleList:
        if not Group.objects.filter(name=role).exists():
            group = Group(name=role)
            group.save()
