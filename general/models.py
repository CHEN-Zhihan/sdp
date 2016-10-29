from django.db import models
from django.contrib.auth.models import User


class Instructor(models.Model):
    _user = models.OneToOneField(User)
    def __str__(self):
        return "{} {}".format(self._user.first_name,self._user.last_name)

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE)
    isOpen = models.BooleanField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    def moveToCategory(self,categoryID):
        newCategory=Category.objects.get(id=categoryID)
        self.category=newCategory
        self.save()

    def addNewModule(self):
        pass

class Module(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    index = models.IntegerField()
    def __str__(self):
        string = "{}:{}".format(self.course.name,self.name)
        return string

class Component(models.Model):
    index = models.IntegerField()
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    typeName = models.CharField(max_length=200)
    content = models.FileField()
    def __str__(self):
        string = "{}-th of {}:{}".format(self.index,self.module.course.name,self.module.name)
        return string

class Participant(models.Model):
    currentCourse = models.ForeignKey(Course,null=True,blank=True,on_delete=models.CASCADE)
    _user = models.OneToOneField(User)
    def __str__(self):
        return "{} {}".format(self._user.first_name,self._user.last_name)
    def enroll(self,courseID):
        self.currentCourse=Course.objects.get(id=courseID)
        self.currentCourse.participant_set.add(self)
        self.save()
        self.currentCourse.save()

class CompletionRecord(models.Model):
    Date = models.DateField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant,on_delete=models.CASCADE)
    def __str__(self):
        return self.course.name
