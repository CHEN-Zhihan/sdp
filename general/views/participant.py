from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from . import authenticate
from ..userModels import Participant
from ..courseModels import Course,Category
from ..exceptions import AlreadyEnrolled
@login_required
def ParticipantIndex(request,participantID):
    participantID=int(participantID)
    if not authenticate.roleCheck(request.user,"Participant",participantID):
        return redirect("myLogout")
    categoryList = Category.getAllCategories()
    participant = Participant.getFromUser(request.user)
    currentCourse=participant.getCurrentCourse()
    progress = -1 if currentCourse==None else int(participant.getProgress()/currentCourse.getTotalProgress()*100)
    completedCourses = participant.getCompletedCourses()
    return render(request,'general/participantIndex.html',{'categoryList':categoryList,'currentCourse':currentCourse,
        "progress":progress,'completedCourses':completedCourses})

@login_required
def showCourseList(request,participantID):
    if authenticate.roleCheck(request.user,"Participant",participantID):
        categoryID = int(request.GET.get("categoryID"))
        category=Category.getByID(categoryID)
        courses = category.getOpenedCourses()
        return render(request,"general/showCourseList.html",{"courses":courses,"category":category})
    return redirect("myLogout")



@login_required
def viewCourse(request,participantID,courseID):
    participantID=int(participantID)
    courseID=int(courseID)
    if authenticate.roleCheck(request.user,"Participant",participantID):
        participant=Participant.getFromUser(request.user)
        if request.method=="GET":
            print("get la!")
            if participant.isTaking(courseID):
                course=participant.getCurrentCourse()
                status="isTaking"
                visibility=participant.getProgress()
                print("is taking this course!")
            elif participant.hasTaken(courseID):
                course=participant.getCompletedCourseByID(courseID)
                status="hasTaken"
                visibility=course.getTotalProgress()
            else:
                course = Course.getByID(courseID)
                status="notTaken"
                visibility=-1
            modules=course.getSortedModules()
            hasEnrolled=participant.hasEnrolled()
            print("all are fine!")
            return render(request,"general/participantCourse.html",{"course":course,"status":status,"modules":modules,"visibility":visibility,"hasEnrolled":hasEnrolled})
        else:
            action = request.POST.get("action")
            if action=="DROP" and participant.isTaking(courseID):
                try:
                    participant.drop()
                except Exception as e:
                    print(e)
                    result=False
                else:
                    result=True
                return JsonResponse({"result":result})
            elif action=="ENROLL" and not participant.hasEnrolled():
                course = Course.getByID(courseID)
                try:
                    result = participant.enroll(course)
                except Exception as e:
                    print(e)
                    result=False
                else:
                    result=True
                return JsonResponse({'result':result})
            elif action=="RETAKE" and not participant.hasEnrolled() and participant.hasTaken(courseID):
                course = participant.getCompletedCourseByID(courseID)
                try:
                    result = participant.retake(course)
                except Exception as e:
                    print(e)
                    result=False
                else:
                    result=True
                return JsonResponse({'result':result})
            return HttpResponse(status=404)
    return redirect("myLogout")

@login_required
def viewModule(request,participantID,courseID,moduleIndex):
    participantID=int(participantID)
    courseID=int(courseID)
    moduleIndex=int(moduleIndex)
    if authenticate.roleCheck(request.user,"Participant",participantID):
        participant = Participant.getFromUser(request.user)
        if participant.canViewModule(courseID,moduleIndex):
            course = participant.getCurrentCourse() if participant.hasEnrolled() else participant.getCompletedCourseByID(courseID)
            module = course.getModuleByIndex(moduleIndex)
            components=module.getSortedComponents()
            return render(request,"general/participantModule.html",{"components":components,"module":module})
        else:
            return HttpResponse(status=404)
    return redirect("myLogout")
    
