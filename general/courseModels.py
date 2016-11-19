from django.db import models
from datetime import datetime
from .exceptions import *
categoryList= ["Mergers and Acquisitions","Markets","Risk Management","Securities","Financial Modelling","Operations","Information Technology"]
class Category(models.Model):
    name = models.CharField(max_length=200)
    @staticmethod
    def getAllCategories():
        return Category.objects.all()

    @staticmethod
    def getByID(ID):
        if Category.objects.filter(id=ID).exists():
            return Category.objects.get(id=ID)
        return None

    def __str__(self):
        return self.name
    def getOpenedCourses(self):
        return self.course_set.filter(_isOpen=True)

for name in categoryList:
    if not Category.objects.filter(name=name).exists():
        category=Category.create(name)
        category.save()

class Enrollment(models.Model):
    class Meta:
        abstract=True
    course = models.ForeignKey('Course',on_delete=models.CASCADE)


class CurrentEnrollment(Enrollment):
    progress = models.IntegerField()
    participant = models.OneToOneField('Participant')


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
    instructor = models.ForeignKey('Instructor',on_delete=models.CASCADE)
    _isOpen = models.BooleanField()
    category = models.ForeignKey('Category',on_delete=models.CASCADE)

    @staticmethod
    def getByID(ID):
        if Course.objects.filter(id=ID).exists():
            return Course.objects.get(id=ID)
        return None

    def isOpen(self):
        return self._isOpen

    def __str__(self):
        return self.name
    
    def _updateIndex(self,newIndex):
        for module in self.module_set.all():
            if module.index>=newIndex:
                module.index+=1
                module.save()
    def updateIndex(self,originIndex,newIndex):
        moduleChanged = self.module_set.get(index=originIndex)
        for module in self.module_set.all():
            if module.index>=newIndex and module.index<originIndex:
                module.index+=1
            elif module.index<=newIndex and module.index>originIndex:
                module.index-=1
            module.save()
        moduleChanged.index=newIndex
        moduleChanged.save()

    def deleteModule(self,module):
        index=module.index
        for component in module.component_set.all():
            module.deleteComponent(component)
        for restModule in self.module_set.all():
            if restModule.index>index:
                restModule-=1
                restModule.save()
        module.delete()

    def modifyModule(self,module,name,description):
        if self.module_set.filter(name=name).exists() and module.name!=name:
            raise NameDuplication()
        module.name=name
        module.description=description
        module.save()

    def createModule(self,name,description,index):
        if self.module_set.filter(name=name).exists():
            raise NameDuplication()
        m=Module()
        m.name=name
        m.description=description
        m.course=self
        self._updateIndex(index)
        m.index=index
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
    
    def getTotalProgress(self):
        return len(self.module_set.all())

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
        if typeName!="TEXT":
            c.content = content
        else:
            c.text = content
        c.save()
        self.component_set.add(c)
        self.save()
        return c
    
    def deleteComponent(self,component):
        index=component.index
        for restComponent in self.component_set.all():
            if restComponent.index>index:
                restComponent.index-=1
                restComponent.save()
        if component.typeName!="TEXT":
            component.content.delete()
        component.delete()

    def _updateIndex(self,newIndex):
        for component in self.component_set.all():
            if component.index>=newIndex:
                component.index+=1
                component.save()

    def updateIndex(self,originIndex,newIndex):
        componentChanged=self.component_set.get(index=originIndex)        
        for component in self.component_set.all():
            if component.index>=newIndex and component.index<originIndex:
                component.index+=1
            elif component.index<=newIndex and component.index>originIndex:
                component.index-=1
            component.save()
        componentChanged.index=newIndex
        componentChanged.save()
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
    text = models.TextField(null=True)
    content = models.FileField(null=True)
    def __str__(self):
        string = "{}-th of {}:{}".format(self.index,self.module.course.name,self.module.name)
        return string
