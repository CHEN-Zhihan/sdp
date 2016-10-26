
from .models import Course,Participant,TakenCourse


def enroll(participantID,courseID):
    participant = Participant.objects.get(pk=participantID)
    course = Course.objects.get(pk=courseID)
    if participant.currentCourse.id==courseID:
        raise Exception("Cannot enroll in currentCourse!")
    if TakenCourse.objects.filter(course=course,participant=participant).exists():
        print("Already taken")
    Course.objects.get(pk=courseID).add(Participant.objects.get(pk=participantID))
