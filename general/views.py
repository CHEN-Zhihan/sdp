from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Course,Participant,CompletedEnrollment,Instructor,Category
from .models import CurrentEnrollment
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

def participantIndex(request,participantID):
    categoryList = Category.objects.all()
    participant = Participant.objects.get(id=participantID)
    try:
        currentEnrollment=participant.currentenrollment
    except ObjectDoesNotExist as e:
        currentCourse=None
    else:
        currentCourse=currentEnrollment.course
    completedCourses = list(map((lambda x:x.course),participant.completedenrollment_set.all()))
    return render(request,'general/participantIndex.html',{'categoryList':categoryList,'currentCourse':currentCourse,\
        'completedCourses':completedCourses})

def showCourseList(request,participantID):
    if request.method=="POST":
        print("handled by showCourseList")
        categoryID = request.POST.get("categoryID")
        courses = Category.objects.get(id=categoryID).getCourses()
        return HttpResponse(
            render_to_string("general/ajax/showCourseList.html",{'courses':courses})
        )

def showCourse(request,participantID):
    if request.method=="POST":
        courseID = request.POST.get('courseID')
        course = Course.objects.get(id=courseID)
        participant = Participant.objects.get(id=participantID)
        modules = course.module_set.all()
        try:
            hasEnrolled = participant.currentenrollment
        except ObjectDoesNotExist as e:
            hasEnrolled=False
        else:
            hasEnrolled=True
        return HttpResponse(
            render_to_string(
                "general/ajax/showCourse.html",
                {'course':course, 'hasEnrolled':hasEnrolled, 'modules':modules}
            )
        )

def enroll(request,participantID):
    if request.method == "POST":
        courseID = request.POST.get('courseID')
        course = Course.objects.get(id=courseID)
        participant = Participant.objects.get(id=participantID)
        result = participant.enroll(course)
        return JsonResponse({'result':result})

def instructorIndex(request,instructorID):
    instructor = Instructor.objects.get(id=instructorID)
    developingCourses = instructor.course_set.filter(_isOpen=False)
    openCourses = instructor.course_set.filter(_isOpen=True)
    return render(request,"general/instructorIndex.html",{'developingCourses':developingCourses,'openCourses':openCourses})

def newCourse(request,instructorID):
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
        return render(request,"general/newCourse.html",{'categories':categories})

def coursePage(request,instructorID,courseID):
    course = Course.objects.get(id=courseID)
    modules = course.module_set.all()
    return render(request,"general/coursePage.html",{'course':course,'modules':modules})

def newModule(request,instructorID,courseID):
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
    else:
        return render(request,"general/newModule.html",{'moduleSet':course.module_set.all()})

def modulePage(request,instructorID,courseID,moduleID):
    course = Course.objects.get(id=courseID)
    module = Module.objects.get(id=moduleID)
    components = module.component_set.all()
    return render(request,"general/modulePage.html",{'course':course,'module':module,'components':components})

def newComponent(request,instructorID,courseID,moduleID):
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

def login(request):
    username=request.POST['username']
    password = request.POST['password']
    user = authenticate(username,password)
    if user is not None:
        login(request,user)
    else:
        return render(request,'general/error.html')
