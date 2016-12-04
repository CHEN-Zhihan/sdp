from datetime import datetime
from django.db import models
from .exceptions import NameDuplication, NoModuleException
import re


class Category(models.Model):
    '''
    Category models the actual category. It has an attribute name and
    a category can get all opened courses under that category.
    '''
    name = models.CharField(max_length=200)

    @staticmethod
    def getAllCategories():
        return Category.objects.all()

    @staticmethod
    def getByID(ID):
        if Category.objects.filter(id=ID).exists():
            return Category.objects.get(id=ID)
        return None

    def getOpenedCourses(self):
        courses = self.course_set.all()
        courses = list(filter((lambda x: x.isOpen()), courses))
        courses.sort(key=(lambda x: x.name))
        return courses

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    '''
    An Enrollment is a abstract class that associate with a course.
    '''
    class Meta:
        abstract = True
    course = models.ForeignKey('Course', on_delete=models.CASCADE)


class CurrentEnrollment(Enrollment):
    '''
    A CurrentEnrollment is an Enrollment that is currently undergoing.
    It is associated with one participant and it contains a progress w.r.t that
    Enrollment. Each participant can only have at most 1 currentEnrollment.
    '''
    progress = models.IntegerField()
    participant = models.OneToOneField('Participant', on_delete=models.CASCADE)

    def __str__(self):
        return "{} taking {}".format(str(self.participant), str(self.course))


class CompletedEnrollment(Enrollment):
    '''
    A CompletedEnrollment is an Enrollment that is completed. It contains a completion date.
    A completedEnrollment is associated with one participant. While a participant can have many
    completedEnrollment.
    '''
    completionDate = models.DateField()
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE)

    @staticmethod
    def createFromCurrentEnrollment(currentEnrollment):
        '''
        Constructor for CompletedEnrollment. It is created from a currentEnrollment.
        The completionDate is the date when this constructor is called.
        '''
        temp = CompletedEnrollment()
        temp.completionDate = datetime.now()
        temp.course = currentEnrollment.course
        temp.course.save()
        temp.participant = currentEnrollment.participant
        temp.participant.save()
        temp.save()
        currentEnrollment.delete()
        return temp

    def __str__(self):
        return "{} completed {} on {}".format(str(self.participant), str(self.course), str(self.completionDate))


class Course(models.Model):
    '''
    A Course contains a name, a description, an isOpen status. It is also associated
    with one instructor and one category.
    '''
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE)
    _isOpen = models.BooleanField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

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

    def _updateIndex(self, newIndex):
        '''
        Method for index update when adding a new module.
        '''
        for module in self.module_set.all():
            if module.index >= newIndex:
                module.index += 1
                module.save()

    def updateIndex(self, originIndex, newIndex):
        '''
        Method for index update when reordering modules.
        '''
        moduleChanged = self.module_set.get(index=originIndex)
        for module in self.module_set.all():
            if module.index >= newIndex and module.index < originIndex:
                module.index += 1
            elif module.index <= newIndex and module.index > originIndex:
                module.index -= 1
            module.save()
        moduleChanged.index = newIndex
        moduleChanged.save()

    def deleteModule(self, module):
        index = module.index
        for restModule in self.module_set.all():
            if restModule.index > index:
                restModule.index -= 1
                restModule.save()
        module.deleteSelf()

    def createModule(self, name, description, index):
        if self.module_set.filter(name=name).exists():
            raise NameDuplication()
        m = Module()
        m.name = name
        m.description = description
        m.course = self
        if index < 0:
            index = 0
        elif index > len(self.module_set.all()):
            index = len(self.module_set.all())
        self._updateIndex(index)
        m.index = index
        m.save()
        self.module_set.add(m)
        self.save()
        return m

    def updateInfo(self, name, category, description):
        if Course.objects.filter(name=name).exists() and self.name != name:
            raise NameDuplication()
        self.name = name
        self.description = description
        self.category = category
        self.save()

    def getSortedModules(self):
        temp = list(self.module_set.all())
        temp.sort(key=(lambda x: x.index))
        return temp

    def openCourse(self):
        if len(self.module_set.all()) == 0:
            raise NoModuleException()
        self._isOpen = True
        self.save()

    def deleteSelf(self):
        while (len(self.module_set.all())):
            temp = list(self.module_set.all()).pop()
            temp.deleteSelf()
        self.delete()

    def getModuleByIndex(self, index):
        if self.module_set.filter(index=index).exists():
            return self.module_set.get(index=index)
        return None

    def hasModule(self, index):
        return self.module_set.filter(index=index).exists()

    def getTotalProgress(self):
        return len(self.module_set.all())


class Module(models.Model):
    '''
    A Module contains a name, a description and an index with in a course which
    it is associated to.
    '''
    name = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    index = models.IntegerField()

    def __str__(self):
        string = "{}:{}".format(self.course.name, self.name)
        return string

    def createComponent(self, typeName, index, content):
        c = lookup[typeName]()
        c.module = self
        if index < 0:
            index = 0
        elif index > len(self._getAllComponents()):
            index = len(self._getAllComponents())
        c.index = index
        self._updateIndex(index)
        c.content = content
        c.save()
        self.save()
        return c

    def deleteComponent(self, component):
        index = component.index
        for restComponent in self._getAllComponents():
            if restComponent.index > index:
                restComponent.index -= 1
                restComponent.save()
        component.deleteSelf()

    def _updateIndex(self, newIndex):
        for component in self._getAllComponents():
            if component.index >= newIndex:
                component.index += 1
                component.save()

    def updateIndex(self, originIndex, newIndex):
        componentChanged = self.getComponentByIndex(originIndex)
        for component in self._getAllComponents():
            if component.index >= newIndex and component.index < originIndex:
                component.index += 1
            elif component.index <= newIndex and component.index > originIndex:
                component.index -= 1
            component.save()
        componentChanged.index = newIndex
        componentChanged.save()

    def getSortedComponents(self):
        components = self._getAllComponents()
        components.sort(key=(lambda x: x.index))
        return components

    def updateInfo(self, name, description):
        if self.course.module_set.filter(name=name).exists() and self.name != name:
            raise NameDuplication()
        self.name = name
        self.description = description
        self.save()

    def hasComponent(self, index):
        return len(list(filter((lambda x: x.index == index), self._getAllComponents()))) != 0

    def getComponentByIndex(self, index):
        return list(filter((lambda x: x.index == index), self._getAllComponents()))[0]

    def deleteSelf(self):
        components = self._getAllComponents()
        while (len(components) != 0):
            temp = components.pop()
            temp.deleteSelf()
        self.delete()

    def _getAllComponents(self):
        fileComponents = list(self.filecomponent_set.all())
        textComponents = list(self.textcomponent_set.all())
        imageComponents = list(self.imagecomponent_set.all())
        videoComponents = list(self.videocomponent_set.all())
        fileComponents.extend(textComponents)
        fileComponents.extend(imageComponents)
        fileComponents.extend(videoComponents)
        return fileComponents


class Component(models.Model):
    '''
    A Component is a abstract class which contains its index within a module
    which it is associated to.
    '''
    class Meta:
        abstract = True
    index = models.IntegerField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        string = "{}-th of {}:{}".format(self.index, self.module.course.name, self.module.name)
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
    content = models.ImageField()

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

    def getContent(self):
        result = "https://www.youtube.com/embed/"
        engine = re.compile('[\W]\w+$')
        return result+engine.findall(self.content)[0][1:]


lookup = {"IMAGE": ImageComponent, "FILE": FileComponent, "TEXT": TextComponent, "VIDEO": VideoComponent}


class ComponentAdapter():
    def __init__(self, component):
        self.typeName = component.getType()
        self.index = component.getIndex()
        self.content = component.getContent()
