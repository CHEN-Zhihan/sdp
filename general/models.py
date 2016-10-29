from django.db import models
from django.contrib.auth.models import User,Group

class SDPUser(models.Model):
    _user = models.OneToOneField(User)
    def create(username,password,first_name,last_name):
        user = SDPUser()
        user._user=User.objects.create_user(username,password=password)
        user._user.first_name=first_name
        user._user.last_name=last_name
        user._user.save()
        user.save()
        return user
    def __str__(self):
        return "{} {}".format(self._user.first_name,self._user.last_name)
    def getID(self):
        return user.id
    def _addToGroup(self,groupID):
        group = Group.objects.get(id=groupID)
        group._user_set.add(self._user)
        self._user.groups.add(group)
    def getGroups(self):
        return _user.groups.all()

class Enrollment(models.Model):
    participant = models.ForeignKey('Participant',on_delete=models.CASCADE)
    course = models.ForeignKey('Course',on_delete=models.CASCADE)
    def create(participant,course):
        enrollment=Enrollment()
        enrollment.participant=participant
        enrollment.course=course
        enrollment.save()
        return enrollment

class CurrentEnrollment(Enrollment):
    progress = models.IntegerField()
    def updateProgess(self,newProgress):
        self.progress=newProgress

class CompletedEnrollment(Enrollment):
    completionDate = models.DateField()


class Instructor(SDPUser):
    def create(username,password,first_name,last_name):
        user = SDPUser.create(username,password,first_name,last_name)
        user._addToGroup(1)
        user.save()
        return user

    def getDevelopingCourses(self):
        return self.course_set.filter(isOpen=False)
    def getOpenCourses(self):
        return self.course_set.filter(isOpen=True)

class Participant(SDPUser):
    current = models.ForeignKey(CurrentEnrollment,on_delete=models.CASCADE,related_name='+')
    completed = models.ForeignKey(CompletedEnrollment,on_delete=models.CASCADE,related_name='+')
    def create(username,password,first_name,last_name):
        user = SDPUser.create(username,password,first_name,last_name)
        user._addToGroup(2)
        user.save()
        return user

class Category(models.Model):
    name = models.CharField(max_length=200)
    def create(name):
        c=Category()
        c.name=name
        return c
    def __str__(self):
        return self.name
    def getCourses(self):
        return self.course_set.all()


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE)
    _isOpen = models.BooleanField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    def create(name,description,instructor,category):
        c=Course()
        c.name=name
        c.description=description
        c.instructor=instructor
        c._isOpen=False
        c.category=category
        c.save()
        return c

    def __str__(self):
        return self.name
    def addModule(self,module):
        module.course=self
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
        m=Module()
        m.name=name
        m.description=description
        m.course=course
        m.index=index
        m.save()
        return m
    def __str__(self):
        string = "{}:{}".format(self.course.name,self.name)
        return string
    def addComponent(self,cid):
        try:
            component = Component.objects.get(id=cid)
            self.component_set.add(component)
            component.module=self
            component.save()
            self.save()
            return True
        except Exception as e:
            return False

class Component(models.Model):
    index = models.IntegerField()
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    typeName = models.CharField(max_length=200)
    content = models.FileField()

    def create(module,typeName,index,content):
        c = Component()
        c.index=index
        c.typeName=typeName
        c.index=index
        c.content=content
        c.save()
        return c

    def __str__(self):
        string = "{}-th of {}:{}".format(self.index,self.module.course.name,self.module.name)
        return string
