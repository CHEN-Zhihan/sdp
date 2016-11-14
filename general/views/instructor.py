from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from ..models import Course,CompletedEnrollment,Instructor,Category
from ..models import CurrentEnrollment, Module, Component
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from . import authenticate
@login_required()
def InstructorIndex(request,instructorID):
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor = Instructor.objects.get(id=instructorID)
        developingCourses = instructor.course_set.filter(_isOpen=False)
        openCourses = instructor.course_set.filter(_isOpen=True)
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
            category = Category.objects.get(id=categoryID)
            instructor = Instructor.objects.get(id=instructorID)
            course = Course.create(name,description,instructor,category)
            result=course!=None
            newID = course.id if result else -1
            return JsonResponse({'result':result,'newCourseID':newID})
        else:
            categories = Category.objects.all()
            return render(request, "general/newCourse.html",{'categories':categories})
    logout(request)
    return redirect("newCourse",instructorID)

@login_required
def coursePage(request,instructorID,courseID):
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.objects.get(id=instructorID)
        if int(courseID) in list(map((lambda x:x.id),instructor.getAllCourses())):
            course = Course.objects.get(id=courseID)
            modules = course.module_set.all()
            return render(request,"general/developCourse.html",{'course':course,'modules':modules})
        else:
            print(courseID,"not in ",list(map((lambda x:x.id),instructor.getAllCourses())))
    logout(request)
    return redirect("coursePage",instructorID,courseID)


@login_required
def newModule(request,instructorID,courseID):
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=instructor.objects.get(id=instructorID)
        if int(courseID) in list(map(lambda x:x.id),instructor.getAllCourses()):
            course = Course.objects.get(id=courseID)
            if request.method == "POST":
                name = request.POST.get('name')
                description = request.POST.get('description')
                index = request.POST.get('index')
                module = Module.create(name,description,course,index)
                if module!=None:
                    course.addModule(module)
                    return JsonResponse({'result':True,'newModuleID':module.id})
                else:
                    return JsonResponse({'result':False,'newModuleID':-1})
    logout(request)
    redirect("newModule",instructorID,courseID)

@login_required
def modulePage(request,instructorID,courseID,moduleID):
    if "Instructor" not in list(map((lambda x:x.name),request.user.groups.all())):
        return redirect('myLogout')
    course = Course.objects.get(id=courseID)
    module = Module.objects.get(id=moduleID)
    components = module.component_set.all()
    return render(request,"general/modulePage.html",{'course':course,'module':module,'components':components})

@login_required
def newComponent(request,instructorID,courseID,moduleID):
    if "Instructor" not in list(map((lambda x:x.name),request.user.groups.all())):
        return redirect('myLogout')
    module = Module.objects.get(id=moduleID)
    if request.method =="POST":
        typeName = request.POST.get('typeName')
        content = request.POST.get('content')
        index = request.POST.get('index')
        component = Component.create(module,typeName,index,content)
        if component!=None:
            module.addComponent(component)
            return JsonResponse({'result':True,'componentID':component.id})
        else:
            return JsonResponse({'result':False,'componentID':-1})
    return HttpResponse(status=404)
