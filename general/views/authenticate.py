from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from ..userModels import Participant,Instructor, HR, Administrator,UserManager

lookup={"Instructor":Instructor,"HR":HR,"Administrator":Administrator,"Participant":Participant}

def myLogin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        userManager = UserManager.getInstance()
        if request.POST.get('action') == 'LOGIN':
            usertype=request.POST.get('usertype')
            user=authenticate(username=username,password=password)
            if user!=None and userManager.userInGroup(user,lookup[usertype]):
                login(request,user)
                uid = userManager.getUserGroupID(user,lookup[usertype])
                return JsonResponse({
                    "result": True,
                    "url": usertype + "/" + str(uid)
                })
            else:
                return JsonResponse({"result": False})
        elif request.POST.get('action') == 'REGISTER':
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            if User.objects.filter(username=username).exists():
                return JsonResponse({"result": False})
            else:
                newUser = userManager.createWithNewUser(username, password, firstName, lastName,Participant)
                login(request,newUser.getUser())
                return JsonResponse({
                    "result": True,
                    "url": "Participant/" + str(newUser.id)
                })
    else:
        return render(request,"general/login.html")

def myLogout(request):
    logout(request)
    return redirect('myLogin')
