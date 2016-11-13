from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from ..models import Participant,Instructor,HR,Administrator
from django.shortcuts import render,redirect
from django.contrib.auth.models import User

def myLogin(request):
    if request.method=="POST":
        username=request.POST.get('username');
        password=request.POST.get('password');
        usertype=request.POST.get('usertype');
        user=authenticate(username=username,password=password)
        if user!=None and usertype in list(map((lambda x:x.name),user.groups.all())):
            login(request,user)
            if usertype=="Instructor":
                instructorID=Instructor.objects.get(_user=user).id
                return redirect('instructorIndex',instructorID)
            elif usertype=="Participant":
                participantID=Participant.objects.get(_user=user).id
                return redirect('participantIndex',participantID)
            elif usertype=="Administrator":
                administratorID=Administrator.objects.get(_user=user).id
                return redirect("administratorIndex",administratorID)
        else:
            print(list(map((lambda x:x.name),user.groups.all())))
            return render(request,"general/login.html")
    else:
        return render(request,"general/login.html");

def myLogout(request):
    logout(request)
    return redirect('myLogin')

def register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        firstName=request.POST.get('firstName')
        lastName=request.POST.get('lastName')
        if User.objects.filter(username=username).exists():
            return render(request,"general/register.html")
        else:
            newParticipant=Participant.create(username,password,firstName,lastName)
            login(request,newParticipant._user)
            return redirect('participantIndex',newParticipant.id)
    else:
        return render(request,"general/register.html")