from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..userModels import Participant, UserManager
from ..courseModels import Course, Category, ComponentAdapter


@login_required
def ParticipantIndex(request, participantID):
    participantID = int(participantID)
    participant = UserManager.getInstance().getFromUser(request.user, Participant, participantID)
    if participant is not None:
        categoryList = Category.getAllCategories()
        currentCourse = participant.getCurrentCourse()
        progress = -1 if currentCourse is None else int(participant.getProgress()/currentCourse.getTotalProgress()*100)
        completedCourses = participant.getCompletedCourses()
        return render(request, 'general/participantIndex.html', {'categoryList': categoryList,
                                                                 'currentCourse': currentCourse,
                                                                 "progress": progress,
                                                                 'completedCourses': completedCourses})
    return redirect("myLogout")


@login_required
def showCourseList(request, participantID):
    participantID = int(participantID)
    participant = UserManager.getInstance().getFromUser(request.user, Participant, participantID)
    if participant is not None:
        if request.GET.get("categoryID") is not None:
            categoryID = int(request.GET.get("categoryID"))
            category = Category.getByID(categoryID)
            if category is not None:
                courses = category.getOpenedCourses()
                categoryList = Category.getAllCategories()
                return render(request, "general/showCourseList.html", {"courses": courses,
                                                                       "categoryList": categoryList,
                                                                       "category": category})
        return HttpResponse(status=404)
    return redirect("myLogout")


@login_required
def viewCourse(request, participantID, courseID):
    participantID = int(participantID)
    courseID = int(courseID)
    participant = UserManager.getInstance().getFromUser(request.user, Participant, participantID)
    if participant is not None:
        if request.method == "GET":
            if participant.isTaking(courseID):
                course = participant.getCurrentCourse()
                status = "isTaking"
                visibility = participant.getProgress()
            elif participant.hasTaken(courseID):
                course = participant.getCompletedCourseByID(courseID)
                status = "hasTaken"
                visibility = course.getTotalProgress()
            else:
                course = Course.getByID(courseID)
                if course is None or not course.isOpen():
                    return HttpResponse(status=404)
                status = "notTaken"
                visibility = -1
            modules = course.getSortedModules()
            hasEnrolled = participant.hasEnrolled()
            categoryList = Category.getAllCategories()
            return render(request, "general/participantCourse.html", {"course": course,
                                                                      "status": status,
                                                                      "modules": modules,
                                                                      "visibility": visibility,
                                                                      "hasEnrolled": hasEnrolled,
                                                                      'categoryList': categoryList})
        else:
            action = request.POST.get("action")
            if action == "DROP" and participant.isTaking(courseID):
                try:
                    participant.drop()
                except Exception as e:
                    print(e)
                    result = False
                else:
                    result = True
                return JsonResponse({"result": result})
            elif action == "ENROLL" and not participant.hasEnrolled():
                course = Course.getByID(courseID)
                try:
                    result = participant.enroll(course)
                except Exception as e:
                    print(e)
                    result = False
                else:
                    result = True
                return JsonResponse({'result': result})
            elif action == "RETAKE" and not participant.hasEnrolled() and participant.hasTaken(courseID):
                course = participant.getCompletedCourseByID(courseID)
                try:
                    result = participant.retake(course)
                except Exception as e:
                    print(e)
                    result = False
                else:
                    result = True
                return JsonResponse({'result': result})
            return HttpResponse(status=404)
    return redirect("myLogout")


@login_required
def viewModule(request, participantID, courseID, moduleIndex):
    participantID = int(participantID)
    courseID = int(courseID)
    moduleIndex = int(moduleIndex)
    participant = UserManager.getInstance().getFromUser(request.user, Participant, participantID)
    if participant is not None:
        if participant.canViewModule(courseID, moduleIndex):
            course = participant.getCurrentCourse() if participant.isTaking(courseID) else participant.getCompletedCourseByID(courseID)
            module = course.getModuleByIndex(moduleIndex)
            if module is None:
                return HttpResponse(status=404)
            components = list(map(ComponentAdapter, module.getSortedComponents()))
            if participant.isTaking(courseID) and moduleIndex == participant.getProgress():
                participant.updateProgress()
            categoryList = Category.getAllCategories()
            return render(request, "general/participantModule.html", {"components": components,
                                                                      "module": module,
                                                                      'categoryList': categoryList})
        else:
            return HttpResponse(status=404)
    return redirect("myLogout")