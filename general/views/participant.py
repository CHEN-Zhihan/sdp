from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from . import authenticate
from ..userModels import Participant
from ..courseModels import Course,Category
@login_required
def ParticipantIndex(request,participantID):
    participantID=int(participantID)
    if not authenticate.roleCheck(request.user,"Participant",participantID):
        return redirect("myLogout")
    categoryList = Category.getAllCategories()
    participant = Participant.getFromUser(request.user)

    try:
        currentEnrollment=participant.currentenrollment
    except ObjectDoesNotExist as e:
        currentCourse=None
    else:
        currentCourse=currentEnrollment.course
    completedCourses = participant.getCompletedCourses()
    return render(request,'general/participantIndex.html',{'categoryList':categoryList,'currentCourse':currentCourse,
        'completedCourses':completedCourses})

@login_required
def showCourseList(request,participantID):
    if not authenticate.roleCheck(request.user,"Participant",participantID):
        return redirect("myLogout")
    if request.method=="POST":
        categoryID = request.POST.get("categoryID")
        courses = Category.getByID(categoryID).getOpenedCourses()
        return HttpResponse(
            render_to_string("general/ajax/showCourseList.html",{'courses':courses})
        )

@login_required
def showCourse(request,participantID):
    if not authenticate.roleCheck(request.user,"Participant",participantID):
        return redirect("myLogout")
    if request.method=="POST":
        courseID = request.POST.get('courseID')
        course = Course.getByID(courseID)
        participant = Participant.getFromUser(request.user)
        modules = course.getSortedModules()
        hasEnrolled = participant.hasEnrolled()
        return HttpResponse(
            render_to_string(
                "general/ajax/showCourse.html",
                {'course':course, 'hasEnrolled':hasEnrolled, 'modules':modules}
            )
        )

@login_required
def enroll(request,participantID):
    if not authenticate.roleCheck(request.user,"Participant",participantID):
        return redirect("myLogout")
    if request.method == "POST":
        courseID = int(request.POST.get('courseID'))
        course = Course.getByID(courseID)
        participant = Participant.getFromUser(request.user)
        result = participant.enroll(course)
        return JsonResponse({'result':result})
    return HttpResponse(status=404)

@login_required
def viewCourse(request,participantID,courseID):
    participantID=int(participantID)
    courseID=int(courseID)
    if authenticate.roleCheck(request.user,"Participant",participantID):
        participant=Participant.getFromUser(request.user)
        if participant.hasCourse(courseID):
            course,status=participant.getCourseByID(courseID)
            modules = course.getSortedModules()
            return HttpResponse(request,"general/viewCourse.html",{"course":course,"status":status,"modules":modules})
    return redirect("myLogout")

@login_required
def viewModule(request,participantID,courseID,moduleIndex):
    participantID=int(participantID)
    courseID=int(courseID)
    moduleIndex=int(moduleIndex)
    if authenticate.roleCheck(request.user,"Participant",participantID):
        participant = Participant.getFromUser(request.user)
        if participant.hasCourse(courseID):
            course,status=participant.getCourseByID(courseID)
            if course.hasModule(moduleIndex) and participant.getProgress()>=moduleIndex:
                module = course.getModuleByIndex(moduleIndex)
                components = module.getSortedComponents()
                return HttpResponse(request,"general/viewModule.html",{"components":components})
    return redirect("myLogout")
