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
            uid = eval(usertype).objects.get(_user=user).id
            return redirect(usertype+"Index",uid)
        else:
            print(list(map((lambda x:x.name),user.groups.all())))
            return render(request,"general/login.html")
    else:
        return render(request,"general/login.html");

def myLogout(request):
    logout(request)
    print("logout la!")
    return redirect('myLogin')

def register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        firstName=request.POST.get('firstName')
        lastName=request.POST.get('lastName')
        usertype = request.POST.get("usertype")
        if User.objects.filter(username=username).exists():
            return render(request,"general/register.html")
        else:
            newUser=eval(usertype).create(username,password,firstName,lastName)
            login(request,newUser._user)
            return redirect(usertype+"Index",newUser.id)
    else:
        return render(request,"general/register.html")

def roleCheck(user,role,passedID):
    if role not in list(map((lambda x:x.name),user.groups.all())):
        print(role,"not in ", user.groups.all())
        return False
    targetUser = eval(role).objects.get(_user=user)
    if int(targetUser.id)!=int(passedID):
        print("user id: ",targetUser.id, "id passed in: ",passedID)
        return False
    return True