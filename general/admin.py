from django.contrib import admin

# Register your models here.
from .models import Course,Category,Component,Instructor,Participant
from .models import Module,TakenCourse

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Component)
admin.site.register(Instructor)
admin.site.register(Participant)
admin.site.register(Module)
admin.site.register(TakenCourse)
