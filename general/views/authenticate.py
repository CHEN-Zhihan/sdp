from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from ..models import Participant,Instructor,HR,Administrator
from django.shortcuts import render,redirect

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
        else:
            print(list(map((lambda x:x.name),user.groups.all())))
            return render(request,"general/login.html")
    else:
        return render(request,"general/login.html");

def myLogout(request):
    logout(request)
    return redirect('myLogin')