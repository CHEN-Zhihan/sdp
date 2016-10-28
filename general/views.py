from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
# Create your views here.

from .models import Course,Participant,Category

def showCatalog(request):
    if request.method == "POST":
        catelog = Category.objects.all()
        result = render_to_string('general/ajax/categories.html', {'category_list':catelog})
        return HttpResponse(result)

def index(request):
    return HttpResponse("Hello, this is View: general.index.")

def participant(request,participantID):
    participant = get_object_or_404(Participant,pk=participantID)

    return render(request,'general/participant.html',{'participant':participant})

def courses(request,courseID, participantID):
    course = get_object_or_404(Course,pk=courseID)
    participant = get_object_or_404(Participant,pk=participantID)
    return render(request,'general/course.html',{'course':course,'participant':participant})
