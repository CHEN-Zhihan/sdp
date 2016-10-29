from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Course,Participant,TakenCourse,Instructor,Category
from django.template.loader import render_to_string


from .models import Course,Participant,CompletionRecord,Instructor

def showCatalog(request):
    if request.method == "POST":
        catelog = Category.objects.all()
        result = render_to_string('general/ajax/categories.html', {'category_list':catelog})
        return HttpResponse(result)

@login_required(login_url="login/")
def index(request):
    return render(request,"index.html")

def participant(request,participantID):
    if not request.user.is_authenticated:
        return render(request,'general/error.html')
    participant = get_object_or_404(Participant,pk=participantID)
    currentCourse = participant.currentCourse
    takenCourses = TakenCourse.objects.filter(participant=participant)
    return render(request,'general/participant.html',{'currentCourse':currentCourse,'takenCourses':takenCourses})

def enrollIn(request,participantID,courseID):
    if not request.user.is_authenticated:
        return render(request,'general/error.html')
    participant = Participant.objects.get(pk=participantID)
    course = Course.objects.get(pk=courseID)
    if participant.currentCourse!=None and participant.currentCourse.id==courseID:
        return render(request,'error.html',{'participant':participant,'currentCourse':currentCourse})
    Course.objects.get(pk=courseID).participant_set.add(Participant.objects.get(pk=participantID))

def instructor(request,instructorID):
    if not request.user.is_authenticated:
        return render(request,'general/error.html')
    instructor = get_object_or_404(Instructor,pk=instructorID)
    myCourses = Course.objects.filter(instructor=instructor)
    developingCourses = myCourses.filter(isOpen=False)
    openCourses = myCourses.filter(isOpen=True)
    return render(request,'instructor.html',{'instructor':instructor,'developingCourses':developingCourses,'openCourses':openCourses})


def courses(request,courseID, participantID):
    course = get_object_or_404(Course,pk=courseID)
    participant = get_object_or_404(Participant,pk=participantID)
    return render(request,'course.html',{'course':course,'participant':participant})

def newCourse(request,instructorID):
    return render(request,'test.html')

def newModule(request,instructorID,courseID):
    pass

def developingCourse(request,instructorID,courseID):
    instructor = get_object_or_404(Instructor,pk=instructorID)
    course = get_object_or_404(Course,pk=courseID)
    return render(request,'general/developingCourse.html',{'instructor':instructor, 'course':course})

def login(request):
    username=request.POST['username']
    password = request.POST['password']
    user = authenticate(username,password)
    if user is not None:
        login(request,user)
    else:
        return render(request,'general/error.html')
