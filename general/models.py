from django.db import models
from django.contrib.auth import login
from django.contrib.auth.models import User,Group
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from abc import ABC,abstractmethod
from .exceptions import *

roleList = ["Instructor","Participant","HR","Administrator"]


for role in roleList:
    if not Group.objects.filter(name=role).exists():
        group = Group(name=role)
        group.save()

class SDPUser(models.Model,ABC):
    _user = models.ForeignKey(User,on_delete=models.CASCADE)

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
        return SDPUser.createFromUser(user,role)

    @staticmethod
    def _getFromUser(user,roleName):
        role=lookup[roleName]
        temp = role.objects.get(_user=user)
        return temp

    def getUser(self):
        return self._user

    def __str__(self):
        return "{} {}".format(self._user.first_name,self._user.last_name)

    def _addToGroup(self,name):
        group = Group.objects.get(name=name)
        group.user_set.add(self._user)
        self._user.groups.add(group)
        group.save()
        self._user.save()
        self.save()

class Enrollment(models.Model,ABC):
    course = models.ForeignKey('Course',on_delete=models.CASCADE)


class CurrentEnrollment(Enrollment):
    progress = models.IntegerField()
    participant = models.OneToOneField('Participant')

    def updateProgess(self,newProgress):
        self.progress=newProgress

    def __str__(self):
        return "{} taking {}".format(str(self.participant),str(self.course))

class CompletedEnrollment(Enrollment):
    completionDate = models.DateField()
    participant = models.ForeignKey('Participant',on_delete=models.CASCADE)

    @staticmethod
    def createFromCurrentEnrollment(currentEnrollment):
        temp = CompletedEnrollment()
        temp.completionDate=datetime.now()
        temp.course=currentEnrollment.course
        temp.course.save()
        temp.participant = currentEnrollment.participant
        temp.participant.save()
        temp.save()
        currentEnrollment.delete()
        return temp

    def __str__(self):
        return "{} completed {} on {}".format(str(self.participant),str(self.course),str(self.completionDate))

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE)
    _isOpen = models.BooleanField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def isOpen(self):
        return self._isOpen

    def __str__(self):
        return self.name
    
    def _updateIndex(self,newIndex):
        for module in self.module_set.all():
            if module.index>=newIndex:
                module.index+=1
                module.save()

    def createModule(self,name,description,index):
        if self.module_set.filter(name=name).exists():
            raise ModulenameDuplication()
        m=Module()
        m.name=name
        m.description=description
        m.course=self
        self._updateIndex(index)
        m.save()
        self.module_set.add(m)
        self.save()
        return m
    def getSortedModules(self):
        temp = list(self.module_set.all())
        temp.sort(key=(lambda x:x.index))
        return temp

    def getInstructor(self):
        return self.instructor

    def openCourse(self):
        if self._isOpen:
            raise Exception("Course {} already opened".format(str(self)))
        self._isOpen=True

    def getModuleByIndex(self,index):
        return self.module_set.get(index=index)

    def hasModule(self,index):
        return self.module_set.filter(index=index).exists()

class Instructor(SDPUser):
    @staticmethod
    def createWithNewUser(username,password,firstName,lastName):
        return SDPUser.createWithNewUser(username,password,firstName,lastName,"Instructor")

    @staticmethod
    def createFromUser(user):
        return SDPUser.createFromUser(user,"Instructor")

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
        if not Course.objects.filter(name=name).exists():
            c=Course()
            c.name=name
            c.description=description
            c.instructor=self
            c._isOpen=False
            c.category=category
            c.save()
            return c
        raise CourseNameDuplication()

    def openCourse(self,course):
        if course in self.course_set.all():
            course._isOpen=True
            course.save()
        else:
            raise NotOwnerException()

    def ownCourse(self,courseID):
        return courseID in list(map((lambda x:x.id),self.getAllCourses()))
    
    def getCourseByID(self,courseID):
        return self.course_set.get(id=courseID)



class Participant(SDPUser):
    @staticmethod
    def createFromUser(user):
        return SDPUser.createFromUser(user,"Participant")

    @staticmethod
    def createWithNewUser(username,password,firstName,lastName):
        return SDPUser.createWithNewUser(username,password,firstName,lastName,"Participant")

    @staticmethod
    def getFromUser(user):
        return SDPUser.getFromUser(user,"Participant")

    def enroll(self,course):
        if self.hasEnrolled():
            raise AlreadyEnrolled()
        self.currentenrollment=CurrentEnrollment()
        self.currentenrollment.course=course
        self.currentenrollment.participant=self
        self.currentenrollment.progress=0
        self.currentenrollment.save()
        self.save()

        return True

    def hasEnrolled(self):
        try:
            hasEnrolled = participant.currentenrollment
        except ObjectDoesNotExist:
            return False
        else:
            return True

    def dropCourse(self):
        if not CurrentEnrollment.objects.filter(participant=self).exists():
            raise NotEnrolledException()
        CurrentEnrollment.objects.filter(participant=self).delete()
        self.currentenrollment=None
        self.save()

    def completeCourse(self):
        self.completedenrollment_set.add(CompletedEnrollment.createFromCurrentEnrollment(self.currentenrollment))
        self.currentenrollment=None
        self.save()

    def getCompletedCourses(self):
        return set(map((lambda x:x.course),self.completedenrollment_set.all()))


class Category(models.Model):
    name = models.CharField(max_length=200)
    @staticmethod
    def create(name):
        c=Category()
        c.name=name
        c.save()
        return c

    @staticmethod
    def getAllCategories():
        return set(map((lambda x:x.name),Category.objects.all()))

    @staticmethod
    def getByID(ID):
        if Category.objects.filter(id=ID).exists():
            return Category.objects.get(id=ID)
        return None

    def __str__(self):
        return self.name
    def getOpenedCourses(self):
        return self.course_set.filter(_isOpen=True)


class Module(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    index = models.IntegerField()

    def __str__(self):
        string = "{}:{}".format(self.course.name,self.name)
        return string

    def createComponent(self,typeName,index,content):
        c = Component()
        c.module=self
        c.index=index
        self._updateIndex(index)
        c.typeName=typeName
        c.content=content
        c.save()
        self.component_set.add(c)
        self.save()
        return c

    def _updateIndex(self,index):
        for component in self.component_set.all():
            if component.index>=newIndex:
                component.index+=1
                component.save()
    
    def getSortedComponents(self):
        components=list(self.component_set.all())
        components.sort(key=(lambda x:x.index))
        return components

    def hasComponent(self,index):
        return self.component_set.filter(index=index).exists()
    
    def getComponentByIndex(self,index):
        return self.component_set.get(index=index)


class Component(models.Model):
    index = models.IntegerField()
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    typeName = models.CharField(max_length=200)
    content = models.FileField()
    def __str__(self):
        string = "{}-th of {}:{}".format(self.index,self.module.course.name,self.module.name)
        return string
    
    def show(self):
        pass


class HR(SDPUser):
    @staticmethod
    def createFromUser(user):
        return SDPUser.createFromUser(user,"HR")
    @staticmethod
    def createWithNewUser(username,password,firstName,lastName):
        return SDPUser.createWithNewUser(username,password,firstName,lastName,"HR")
    @staticmethod
    def getFromUser(user):
        return SDPUser.getFromUser(user,"HR")


class Administrator(SDPUser):
    @staticmethod
    def createWithNewUser(username,password,firstName,lastName):
        return SDPUser.createWithNewUser(username,password,firstName,lastName,"Administrator")

    @staticmethod
    def createFromUser(user):
        return SDPUser.createFromUser(user,"Administrator")

    @staticmethod
    def designate(user,role):
        return SDPUser.createFromUser(user,role)

    @staticmethod
    def getFromUser(user):
        return SDPUser.getFromUser(user,"Administrator")

    @staticmethod
    def getUserGroups(user):
        return list(map((lambda x:x.name),user.groups.all()))

lookup = {"Instructor":Instructor,"Participant":Participant,"HR":HR,"Administrator":Administrator}
