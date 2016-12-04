from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from .exceptions import NameDuplication
from .courseModels import Category, Course, CurrentEnrollment, CompletedEnrollment


class SDPUser(models.Model):
    '''
    SDPUser is an abstract class used as an interface to the User model
    provided by Django.
    '''
    _user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def setUser(self, user):
        self._user = user

    def getUser(self):
        return self._user

    def __str__(self):
        return "{} {}".format(self._user.first_name, self._user.last_name)


class Instructor(SDPUser):
    '''
    An Instructor is an SDPUser who can create courses.
    '''

    def getDevelopingCourses(self):
        return list(filter((lambda x: not x.isOpen()), self.course_set.all()))

    def getOpenedCourses(self):
        return list(filter((lambda x: x.isOpen()), self.course_set.all()))

    def getAllCourses(self):
        return self.course_set.all()

    def createCourse(self, name, description, category):
        if Course.objects.filter(name=name).exists():
            raise NameDuplication()
        c = Course()
        c.name = name
        c.description = description
        c.instructor = self
        c._isOpen = False
        c.category = category
        c.save()
        return c

    def ownCourse(self, courseID):
        return courseID in list(map((lambda x: x.id), self.getAllCourses()))

    def getCourseByID(self, courseID):
        return self.course_set.get(id=courseID)


class Participant(SDPUser):
    '''
    A Participant is an SDPUser that can enroll, view, drop, retake courses.
    '''
    def enroll(self, course):
        self.currentenrollment = CurrentEnrollment()
        self.currentenrollment.course = course
        self.currentenrollment.participant = self
        self.currentenrollment.progress = 0
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
        if self.currentenrollment.progress >= self.currentenrollment.course.getTotalProgress()-1:
            self._complete()
        else:
            self.currentenrollment.progress += 1
            self.currentenrollment.save()
            self.save()

    def drop(self):
        CurrentEnrollment.objects.filter(participant=self).delete()
        self.currentenrollment = None
        self.save()

    def retake(self, course):
        completedEnrollment = self.completedenrollment_set.get(course=course)
        completedEnrollment.delete()
        self.save()
        self.enroll(course)

    def hasTaken(self, courseID):
        return len(list(filter((lambda x: x.id == courseID), self.getCompletedCourses()))) != 0

    def isTaking(self, courseID):
        return self.hasEnrolled() and self.currentenrollment.course.id == courseID

    def _complete(self):
        self.completedenrollment_set.add(CompletedEnrollment.createFromCurrentEnrollment(self.currentenrollment))
        self.currentenrollment = None
        self.save()

    def canViewModule(self, courseID, moduleIndex):
        if self.hasTaken(courseID):
            return True
        if self.isTaking(courseID) and self.getProgress() >= moduleIndex:
            return True
        return False

    def getCompletedCourses(self):
        return set(map((lambda x: x.course), self.completedenrollment_set.all()))

    def getCompletedCourseByID(self, courseID):
        for completed in self.getCompletedCourses():
            if completed.id == courseID:
                return completed

    def getCurrentCourse(self):
        if self.hasEnrolled():
            return self.currentenrollment.course
        return None


class HR(SDPUser):
    pass


class Administrator(SDPUser):
    '''
    An Administrator is an SDPUser who can desigate a newRole
    to a exist user.
    '''
    def designate(self, user, newRole):
        return UserManager.getInstance().createFromUser(user, newRole)


class UserManager():
    '''
    A UserManager is a singleton class that can
    get an SDPUser from a User in Django, judge whether a user is in a group,
    get an SDPUser id from a User in a Group, create a new user in a group and
    create a new SDPUser from a exist user in a new group.
    '''
    _instance = None

    @staticmethod
    def getInstance():
        if UserManager._instance is None:
            UserManager._instance = UserManager()
        return UserManager._instance

    def getFromUser(self, user, group, ID):
        if self.userInGroup(user, group):
            if group.objects.filter(id=ID).exists():
                temp = group.objects.get(id=ID)
                if temp.getUser().id == user.id:
                    return temp
        return None

    def userInGroup(self, user, group):
        return group.__name__ in list(map((lambda x: x.name), user.groups.all()))

    def getUserGroupID(self, user, group):
        return list(filter((lambda x: x.getUser().id == user.id), group.objects.all()))[0].id

    def createWithNewUser(self, username, password, firstName, lastName, group):
        user = User.objects.create_user(username=username, password=password, first_name=firstName, last_name=lastName)
        user.save()
        return self.createFromUser(user, group)

    def createFromUser(self, user, group):
        temp = group()
        temp.setUser(user)
        temp.save()
        temp.getUser().groups.add(Group.objects.get(name=group.__name__))
        return temp
