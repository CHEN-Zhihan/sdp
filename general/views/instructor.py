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
        openCourses = instructor.getDevelopingCourses()
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
                result = True
            except CourseNameDuplication:
                result = False
            newID = course.id if result else -1
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
            modules = course.getSortedModules()
            return render(request,"general/developCourse.html",{'course':course,'modules':modules})
        else:
            print(courseID,"not in ",list(map((lambda x:x.id),instructor.getAllCourses())))
    logout(request)
    return redirect("coursePage",instructorID,courseID)


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
                index = request.POST.get('index')
                module = Module.create(name,description,course,index)
                if module!=None:
                    course.addModule(module)
                    return JsonResponse({'result':True})
                else:
                    return JsonResponse({'result':False})
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
                return render(request,"general/modulePage.html",{'course':course,'module':module,'components':components})

@login_required
def newComponent(request,instructorID,courseID,moduleIndex):
    courseID=int(courseID)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course=instructor.getCourseByID(courseID)
            if course.hasModule(int(moduleIndex)):
                module=course.getModuleByIndex(moduleIndex)
                if request.method =="POST":
                    typeName = request.POST.get('typeName')
                    content = request.POST.get('content')
                    index = request.POST.get('index')
                    component = module.createComponent(module,typeName,index,content)
                    return JsonResponse({'result':True,'componentID':component.index})
    return HttpResponse(status=404)
