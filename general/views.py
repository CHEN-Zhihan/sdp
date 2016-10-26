from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
# Create your views here.

from .models import Course,Participant

def index(request):
    return HttpResponse("Hello, this is View: general.index.")

def participant(request,participantID):
    participant = get_object_or_404(Participant,pk=participantID)
    return render(request,'general/participant.html',{'participant':participant})
    return HttpResponse("You're looking at participant {}".format(participant.name))
def courses(request,participantID):
    return HttpResponse("You're looking at participant {}'s courses".format(participantID))
