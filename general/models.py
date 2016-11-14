from django.db import models
from django.contrib.auth.models import User,Group
from datetime import datetime


roleList = ["Instructor","Participant","HR","Administrator"]

for role in roleList:
    if not Group.objects.filter(name=role).exists():
        group = Group(name=role)
        group.save()

class SDPUser(models.Model):
    _user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        abstract=True
    def create(username,password,first_name,last_name):
        user = SDPUser()
        user._user=User.objects.create_user(username,password=password,first_name=first_name,last_name=last_name)
        user._user.save()
        user.save()
        return user

    def __str__(self):
        return "{} {}".format(self._user.first_name,self._user.last_name)
    def getID(self):
        return user.id

    def _addToGroup(self,name):
        group = Group.objects.get(name=name)
        group.user_set.add(self._user)
        self._user.groups.add(group)
        group.save()
        self._user.save()
        self.save()
    def getGroups(self):
        return map((lambda x:x.name),self._user.groups.all())

class Enrollment(models.Model):
    course = models.ForeignKey('Course',on_delete=models.CASCADE)
    class Meta:
        abstract=True

class CurrentEnrollment(Enrollment):
    progress = models.IntegerField()
    participant = models.OneToOneField('Participant')
    def updateProgess(self,newProgress):
        self.progress=newProgress
    def create(course,participant):
        e = CurrentEnrollment()
        e.course=course
        e.participant=participant
        e.participant.save()
        e.progress=0
        e.save()
        return e
    def __str__(self):
        return "{} taking {}".format(str(self.participant),str(self.course))

class CompletedEnrollment(Enrollment):
    completionDate = models.DateField()
    participant = models.ForeignKey('Participant',on_delete=models.CASCADE)
    def createFromCurrentEnrollment(currentEnrollment,date):
        temp = CompletedEnrollment()
        temp.completionDate=date
        temp.course=currentEnrollment.course
        temp.course.save()
        temp.participant = currentEnrollment.participant
        temp.participant.save()
        temp.save()
        currentEnrollment.delete()
        return temp

    def __str__(self):
        return "{} completed {} on {}".format(str(self.participant),str(self.course),str(self.completionDate))

class Instructor(SDPUser):
    def create(username,password,first_name,last_name):
        instructor = Instructor()
        instructor._user=User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name)
        instructor._addToGroup("Instructor")
        instructor.save()
        return instructor
    def getDevelopingCourses(self):
        return self.course_set.filter(_isOpen=False)
    def getOpenedCourses(self):
        return self.course_set.filter(_isOpen=True)
    def getAllCourses(self):
        return self.course_set.all()

    def openCourse(course):
        if course in self.course_set.all():
            course._isOpen=True
            course.save()
        else:
            raise Exception("Unable to open course {}, not created by {}".format(str(course),str(self)))

    def _add(user):
        user._addToGroup("Instructor")

class Participant(SDPUser):
    def create(username,password,first_name,last_name):
        p=Participant()
        p._user=User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name)
        p._addToGroup("Participant")
        p.save()
        return p
    def enroll(self,course):
        self.currentenrollment = CurrentEnrollment.create(course,self)
        self.save()
        return True

    def hasEnrolled(self):
        try:
            hasEnrolled = participant.currentenrollment
        except ObjectDoesNotExist as e:
            return False
        else:
            return True

    def dropCourse(self):
        CurrentEnrollment.objects.filter(participant=self).delete()
        self.currentenrollment=None
        self.save()

    def completeCourse(self):
        self.completedenrollment_set.add(CompletedEnrollment.createFromCurrentEnrollment(self.currentenrollment,datetime.now()))
        self.currentenrollment=None
        self.save()

    def getCompletedCourses(self):
        return set(map((lambda x:x.course),self.completedenrollment_set.all()))


class Category(models.Model):
    name = models.CharField(max_length=200)
    def create(name):
        c=Category()
        c.name=name
        c.save()
        return c
    def __str__(self):
        return self.name
    def getOpenedCourses(self):
        return self.course_set.filter(_isOpen=True)


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE)
    _isOpen = models.BooleanField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    def create(name,description,instructor,category):
        try:
            c=Course()
            c.name=name
            c.description=description
            c.instructor=instructor
            c._isOpen=False
            c.category=category
            c.save()
            return c
        except Exception as e:
            print(e)
            return None

    def isOpen(self):
        return self._isOpen

    def __str__(self):
        return self.name
    def addModule(self,module):
        self.module_set.add(module)
        module.save()
        self.save()
    def getInstructor(self):
        return self.instructor


class Module(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    index = models.IntegerField()
    def create(name,description,course,index):
        try:
            m=Module()
            m.name=name
            m.description=description
            m.course=course
            m.index=index
            m.save()
            return m
        except Exception as e:
            print(e)
            return None
    def __str__(self):
        string = "{}:{}".format(self.course.name,self.name)
        return string
    def addComponent(self,component):
        self.component_set.add(component)
        component.save()
        self.save()

class Component(models.Model):
    index = models.IntegerField()
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    typeName = models.CharField(max_length=200)
    content = models.FileField()

    def create(module,typeName,index,content):
        c = Component()
        c.module=module
        c.index=index
        c.typeName=typeName
        c.content=content
        c.save()
        return c
    def __str__(self):
        string = "{}-th of {}:{}".format(self.index,self.module.course.name,self.module.name)
        return string

class HR(SDPUser):

    def create(username,password,firstName,lastName):
        hr = HR()
        hr._user=User.objects.create_user(username=username,password=password,first_name=firstName,last_name=lastName)
        hr._user.save()
        hr._addToGroup("HR")
        return hr

    def _add(user):
        user._addToGroup("HR")

class Administrator(SDPUser):
    def create(username,password,firstName,lastName):
        admin = Administrator()
        admin._user=User.objects.create_user(username=username,password=password,first_name=firstName,last_name=lastName)
        admin._user.save()
        admin._addToGroup("Administrator")
        return admin

    def _add(user):
        user._addToGroup("Administrator")

    def designate(username,role):
        newUser = role()
        newUser._user = User.objects.get(username=username)
        newUser._user.save()
        role._add(newUser)
        newUser.save()
        return newUser
