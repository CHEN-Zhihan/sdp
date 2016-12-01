from datetime import datetime
from django.db import models
from .exceptions import NameDuplication,NoModuleException
categoryList= ["Mergers and Acquisitions","Markets","Risk Management","Securities",
"Financial Modelling","Operations","Information Technology"]
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
        category=Category()
        category.name=name
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
    
    @staticmethod
    def getAllCourses():
        return Course.objects.all()

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
        for restModule in self.module_set.all():
            if restModule.index>index:
                restModule-=1
                restModule.save()
        module.deleteSelf()


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

    def updateInfo(self,name,category,description):
        if Course.objects.filter(name=name).exists() and self.name!=name:
            raise NameDuplication()
        self.name=name
        self.description=description
        self.category=category
        self.save()

    def getSortedModules(self):
        temp = list(self.module_set.all())
        temp.sort(key=(lambda x:x.index))
        return temp


    def openCourse(self):
        if len(self.module_set.all())==0:
            raise NoModuleException()
        self._isOpen=True
        self.save()

    def deleteSelf(self):
        while (len(self.module_set.all())):
            temp = self.module_set.pop()
            temp.deleteSelf()
        self.delete()

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
        c = lookup[typeName]()
        print(type(c))
        c.module=self
        c.index=index
        self._updateIndex(index)
        c.content=content
        c.save()
        self.save()
        return c

    def deleteComponent(self,component):
        index=component.index
        for restComponent in self._getAllComponents():
            if restComponent.index>index:
                restComponent.index-=1
                restComponent.save()
        component.deleteSelf()

    def _updateIndex(self,newIndex):
        for component in self._getAllComponents():
            if component.index>=newIndex:
                component.index+=1
                component.save()

    def updateIndex(self,originIndex,newIndex):
        componentChanged=self.getComponentByIndex(originIndex)        
        for component in self._getAllComponents():
            if component.index>=newIndex and component.index<originIndex:
                component.index+=1
            elif component.index<=newIndex and component.index>originIndex:
                component.index-=1
            component.save()
        componentChanged.index=newIndex
        componentChanged.save()

    def getSortedComponents(self):
        components = self._getAllComponents()
        components.sort(key=(lambda x:x.index))
        return components

    def updateInfo(self,name,description):
        if self.course.module_set.filter(name=name).exists() and self.name!=name:
            raise NameDuplication()
        self.name=name
        self.description=description
        self.save()

    def hasComponent(self,index):
        return self.filecomponent_set.filter(index=index).exists() or self.textcomponent_set.filter(index=index).exists()\
            or self.imagecomponent_set.filter(index=index).exists()

    def getComponentByIndex(self,index):
        if self.filecomponent_set.filter(index=index).exists():
            return self.filecomponent_set.get(index=index)
        elif self.textcomponent_set.filter(index=index).exists():
            return self.textcomponent_set.get(index=index)
        elif self.imagecomponent_set.filter(index=index).exists():
            return self.imagecomponent_set.get(index=index)

    def deleteSelf(self):
        components = self._getAllComponents()
        while (len(components)!=0):
            temp = components.pop()
            temp.deleteSelf()
        self.delete()
    
    def _getAllComponents(self):
        fileComponents=list(self.filecomponent_set.all())
        textComponents = list(self.textcomponent_set.all())
        imageComponents = list(self.imagecomponent_set.all())
        fileComponents.extend(textComponents) 
        fileComponents.extend(imageComponents)
        return fileComponents

class Component(models.Model):
    class Meta:
        abstract=True
    index = models.IntegerField()
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    def __str__(self):
        string = "{}-th of {}:{}".format(self.index,self.module.course.name,self.module.name)
        return string


    def getIndex(self):
        return self.index

    def getContent(self):
        return self.content

class TextComponent(Component):
    content = models.TextField()

    def deleteSelf(self):
        self.delete()

    def getType(self):
        return "TEXT"



class FileComponent(Component):
    content = models.FileField()
    def deleteSelf(self):
        self.content.delete()
        self.delete()

    def getType(self):
        return "FILE"

class ImageComponent(Component):
    content = models.ImageField(null=True,blank=True)

    def deleteSelf(self):
        self.content.delete()
        self.delete()

    def getType(self):
        return "IMAGE"

class VideoComponent(Component):
    content = models.URLField()
    def getType(self):
        return "VIDEO"
    def deleteSelf(self):
        self.delete()

lookup={"IMAGE":ImageComponent,"FILE":FileComponent,"TEXT":TextComponent,"VIDEO":VideoComponent}