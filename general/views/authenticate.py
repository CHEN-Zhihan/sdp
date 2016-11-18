from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from ..models import Participant,Instructor, HR, Administrator

lookup={"Instructor":Instructor,"HR":HR,"Administrator":Administrator,"Participant":Participant}

def myLogin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        usertype=request.POST.get('usertype')
        user=authenticate(username=username,password=password)
        if user!=None and usertype in list(map((lambda x:x.name),user.groups.all())):
            login(request,user)
            uid = lookup[usertype].objects.get(_user=user).id
            return redirect(usertype+"Index",uid)
        else:
            return render(request,"general/login.html")
    else:
        return render(request,"general/login.html")

def myLogout(request):
    logout(request)
    print("logout la!")
    return redirect('myLogin')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        if User.objects.filter(username=username).exists():
            return render(request, "general/register.html")
        else:
            newUser = Participant.createWithNewUser(username, password, firstName, lastName)
            login(request,newUser.getUser())
            return redirect("ParticipantIndex", newUser.id)
    else:
        return render(request, "general/register.html")

def roleCheck(user,role,passedID):
    if role!=None:
        if role not in Administrator.getUserGroups(user):
            print(role,"not in ", Administrator.getUserGroups(user))
            return False
        targetUser = Administrator.getFromUser(user,role)
        if int(targetUser.id)!=int(passedID):
            print("user id: ",targetUser.id, "id passed in: ",passedID)
            return False
        return True
    return False
