from django.db import models
from django.contrib.auth.models import User,Group
from django.core.exceptions import ObjectDoesNotExist
from .exceptions import *
from .courseModels import Category,Course,CurrentEnrollment,CompletedEnrollment


roleList = ["Instructor","Participant","HR","Administrator"]
for role in roleList:
    if not Group.objects.filter(name=role).exists():
        group = Group(name=role)
        group.save()

class SDPUser(models.Model):
    _user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        abstract=True
    @staticmethod
    def _createFromUser(user,role):
        temp=lookup[role]()
        temp._user=user
        temp._addToGroup(role)
        temp.save()
        return temp

    @staticmethod
    def _createWithNewUser(username,password,firstName,lastName,role):
        user=User.objects.create_user(username=username,password=password,first_name=firstName,last_name=lastName)
        return SDPUser._createFromUser(user,role)

    @staticmethod
    def getFromUser(user,roleName):
        role=lookup[roleName]
        temp = role.objects.get(_user=user)
        return temp

    def getUser(self):
        return self._user

    def __str__(self):
        return "{} {}".format(self._user.first_name,self._user.last_name)


    def _addToGroup(self,name):
        print(name)
        group = Group.objects.get(name=name)
        group.user_set.add(self._user)
        self._user.groups.add(group)
        group.save()
        self._user.save()
        self.save()

class Instructor(SDPUser):
    @staticmethod
    def createWithNewUser(username,password,firstName,lastName):
        return SDPUser._createWithNewUser(username,password,firstName,lastName,"Instructor")

    @staticmethod
    def createFromUser(user):
        return SDPUser._createFromUser(user,"Instructor")

    @staticmethod
    def getFromUser(user):
        return SDPUser.getFromUser(user,"Instructor")

    def getDevelopingCourses(self):
        return self.course_set.filter(_isOpen=False)

    def getOpenedCourses(self):
        return self.course_set.filter(_isOpen=True)

    def getAllCourses(self):
        return self.course_set.all()

    def createCourse(self,name,description,category):
        if Course.objects.filter(name=name).exists():
            raise NameDuplication()            
        c=Course()
        c.name=name
        c.description=description
        c.instructor=self
        c._isOpen=False
        c.category=category
        c.save()
        return c
    
    def deleteCourse(self,course):
        for module in course.getSortedModules():
            for component in module.getSortedComponents():
                component.delete()
            module.delete()
        course.delete()

    def modifyCourse(self,course,name,description,category):
        if Course.objects.filter(name=name).exists() and course.name!=name:
            raise NameDuplication()
        course.name=name
        course.description=description
        course.category=category
        course.save()

    def openCourse(self,course):
        course._isOpen=True
        course.save()

    def ownCourse(self,courseID):
        return courseID in list(map((lambda x:x.id),self.getAllCourses()))

    def getCourseByID(self,courseID):
        return self.course_set.get(id=courseID)

class Participant(SDPUser):
    @staticmethod
    def createFromUser(user):
        return SDPUser._createFromUser(user,"Participant")

    @staticmethod
    def createWithNewUser(username,password,firstName,lastName):
        return SDPUser._createWithNewUser(username,password,firstName,lastName,"Participant")

    @staticmethod
    def getFromUser(user):
        return SDPUser.getFromUser(user,"Participant")

    def enroll(self,course):
        self.currentenrollment=CurrentEnrollment()
        self.currentenrollment.course=course
        self.currentenrollment.participant=self
        self.currentenrollment.progress=0
        self.currentenrollment.save()
        self.save()

    def getProgress(self):
        if self.hasEnrolled():
            return self.currentenrollment.progress
        return -1

    def hasEnrolled(self):
        try:
            _ = self.currentenrollment
        except ObjectDoesNotExist:
            return False
        else:
            return True

    def updateProgress(self):
        if self.currentenrollment.progress>=self.currentenrollment.course.getTotalProgress()-1:
            self.complete()
        else:
            self.currentenrollment.progress+=1
            self.currentenrollment.save()
            self.save()
            print("now can visit",self.currentenrollment.progress)

    def drop(self):
        CurrentEnrollment.objects.filter(participant=self).delete()
        self.currentenrollment=None
        self.save()

    def retake(self,course):
        completedEnrollment = self.completedenrollment_set.get(course=course)
        completedEnrollment.delete()
        self.save()
        self.enroll(course)

    def hasTaken(self,courseID):
        return len(list(filter((lambda x:x.id==courseID),self.getCompletedCourses())))!=0

    def isTaking(self,courseID):
        return self.hasEnrolled() and self.currentenrollment.course.id==courseID

    def complete(self):
        self.completedenrollment_set.add(CompletedEnrollment.createFromCurrentEnrollment(self.currentenrollment))
        self.currentenrollment=None
        self.save()
    
    def canViewModule(self,courseID,moduleIndex):
        if self.hasTaken(courseID):
            return True
        if self.isTaking(courseID) and self.getProgress()>=moduleIndex:
            return True
        return False

    def getCompletedCourses(self):
        return set(map((lambda x:x.course),self.completedenrollment_set.all()))

    def getByID(self,ID):
        if Participant.objects.filter(id=ID).exists():
            return Participant.objects.get(id=ID)
        return None

    def getCompletedCourseByID(self,courseID):
        for completed in self.getCompletedCourses():
            if completed.id==courseID:
                return completed
    def getCurrentCourse(self):
        if self.hasEnrolled():
            return self.currentenrollment.course
        return None

class HR(SDPUser):
    @staticmethod
    def createFromUser(user):
        return SDPUser._createFromUser(user,"HR")
    @staticmethod
    def createWithNewUser(username,password,firstName,lastName):
        return SDPUser._createWithNewUser(username,password,firstName,lastName,"HR")
    @staticmethod
    def getFromUser(user):
        return SDPUser.getFromUser(user,"HR")


class Administrator(SDPUser):
    @staticmethod
    def createWithNewUser(username,password,firstName,lastName):
        return SDPUser._createWithNewUser(username,password,firstName,lastName,"Administrator")

    @staticmethod
    def createFromUser(user):
        return SDPUser._createFromUser(user,"Administrator")

    @staticmethod
    def designate(user,newRole):
        return SDPUser._createFromUser(user,newRole)

    @staticmethod
    def getFromUser(user):
        return SDPUser.getFromUser(user,"Administrator")

    @staticmethod
    def getUserGroups(user):
        return list(map((lambda x:x.name),user.groups.all()))

    @staticmethod
    def createCategory(name):
        if Category.objects.filter(name=name).exists():
            raise NameDuplication()
        c=Category()
        c.name=name
        c.save()
        return c

lookup = {"Instructor":Instructor,"Participant":Participant,"HR":HR,"Administrator":Administrator}
