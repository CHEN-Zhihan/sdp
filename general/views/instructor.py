from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from ..models import Course,CompletedEnrollment,Instructor,Category
from ..models import CurrentEnrollment, Module, Component,Administrator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from . import authenticate
from ..exceptions import *

@login_required
def InstructorIndex(request,instructorID):
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor = Instructor.getFromUser(request.user)
        developingCourses = instructor.getDevelopingCourses()
        openCourses = instructor.getOpenedCourses()
        return render(request,"general/instructorIndex.html",{'developingCourses':developingCourses,'openCourses':openCourses})
    logout(request)
    return redirect("InstructorIndex",instructorID)

@login_required
def newCourse(request,instructorID):
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        if request.method == "POST":
            name = request.POST.get('name')
            description = request.POST.get("description")
            categoryID = request.POST.get("categoryID")
            category = Category.getByID(categoryID)
            instructor = Instructor.getFromUser(request.user)
            try:
                course = instructor.createCourse(name,description,category)
            except NameDuplication:
                result = False
                newID=-2
            except Exception:
                result = False
                newID=-1
            else:
                result = True
                newID=course.id
            return JsonResponse({'result':result,'newCourseID':newID})
        else:
            categories = Category.getAllCategories()
            return render(request, "general/newCourse.html",{'categories':categories})
    logout(request)
    return redirect("newCourse",instructorID)

@login_required
def coursePage(request,instructorID,courseID):
    courseID=int(courseID)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if request.method=="POST":
                action = request.POST.get("action")
                if action=="OPEN":
                    try:
                        instructor.openCourse(course)
                    except Exception:
                        result=False
                    else:
                        result=True
                    return JsonResponse({"result":result})
                elif action=="DELETE":
                    try:
                        instructor.deleteCourse(course)
                    except Exception:
                        result=False
                    else:
                        result=True
                    return JsonResponse({"result":result})
            if request.method=="GET":
                modules = course.getSortedModules()
                return render(request,"general/developCourse.html",{'course':course,'modules':modules,"isOpen":course.isOpen()})
        else:
            print(courseID,"not in ",list(map((lambda x:x.id),instructor.getAllCourses())))
    logout(request)
    return redirect("coursePage",instructorID,courseID)


@login_required
def changeModuleOrder(request,instructorID,courseID):
    instructorID=int(instructorID)
    courseID=int(courseID)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if request.method=="POST":
                originIndex = request.POST.get("originIndex")
                newIndex = request.POST.get("newIndex")
                try:
                    course.updateIndex(originIndex,newIndex)
                except Exception:
                    result=False
                else:
                    result=True
                return JsonResponse({"result":result})
            else:
                return HttpResponse(status=404)
    redirect("myLogout")


@login_required
def modifyCourse(request,instructorID,courseID):
    courseID=int(courseID)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if request.method=="POST":
                name=request.POST.get("name")
                description = request.POST.get("description")
                categoryID = request.POST.get("categoryID")
                category = Category.getByID(categoryID)
                try:
                    instructor.modifyCourse(name,description,category)
                except NameDuplication:
                    errno=-2
                except Exception:
                    errno=-1
                else:
                    errno=0
                return JsonResponse({"result":errno})
            else:
                return render(request,"general/modifyCourse.html",{"course":course})


@login_required
def newModule(request,instructorID,courseID):
    courseID=int(courseID)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course =instructor.getCourseByID(courseID)
            if request.method == "POST":
                name = request.POST.get('name')
                description = request.POST.get('description')
                index = int(request.POST.get('index'))
                try:
                    module = course.createModule(name,description,index)
                except NameDuplication:
                    newIndex=-2
                    result=False
                except Exception:
                    newIndex=-1
                    result=False
                else:
                    newIndex=module.index
                    result=True
                return JsonResponse({'result':result,"newModuleIndex":newIndex})
            elif request.method == "GET":
                return render(request, "general/newModule.html")
    logout(request)
    redirect("newModule",instructorID,courseID)

@login_required
def modulePage(request,instructorID,courseID,moduleIndex):
    courseID=int(courseID)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course=instructor.getCourseByID(courseID)
            module = course.getModuleByIndex(moduleIndex)
            if module!=None:
                components = module.getSortedComponents()
                return render(request,"general/modulePage.html",{'course':course,'module':module,'components':components,"isOpen":course.isOpen()})


@login_required
def newComponent(request,instructorID,courseID,moduleIndex):
    courseID=int(courseID)
    moduleIndex=int(moduleIndex)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course=instructor.getCourseByID(courseID)
            if course.hasModule(moduleIndex):
                module=course.getModuleByIndex(moduleIndex)
                if request.method =="POST":
                    typeName = request.POST.get('typeName')
                    content = request.POST.get('content')
                    index = request.POST.get('index')
                    component = module.createComponent(typeName,index,content)
                    return JsonResponse({'result':True,'componentID':component.index})
    return HttpResponse(status=404)


@login_required
def changeComponentOrder(request,instructorID,courseID,moduleIndex):
    instructorID=int(instructorID)
    courseID=int(courseID)
    moduleIndex=int(moduleIndex)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if course.hasModule(moduleIndex):
                module=course.getModuleByIndex(moduleIndex)
                if request.method=="POST":
                    originIndex = request.POST.get("originIndex")
                    newIndex = int(request.POST.get("newIndex"))
                    try:
                        module.updateIndex(originIndex,newIndex)
                    except Exception:
                        result=False
                    else:
                        result=True
                    return JsonResponse({"result":result})
                else:
                    return HttpResponse(status=404)
    return redirect("myLogout")
