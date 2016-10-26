from django.db import models

class Instructor(models.Model):
    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

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
    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    currentCourse = models.ForeignKey(Course,null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class TakenCourse(models.Model):
    completionDate = models.DateField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant,on_delete=models.CASCADE)

    def __str__(self):
        participant = self.participant.name
        course = self.course.name
        date = str(self.completionDate)
        return "{participant} completed {course} on {date}".format(participant=participant,course=course,date=date)
