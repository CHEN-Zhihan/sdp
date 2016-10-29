from django.contrib import admin

# Register your models here.
from .models import Course,Category,Component,Instructor,Participant
from .models import Module,CurrentEnrollment,Enrollment,CompletedEnrollment
from .models import SDPUser

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Component)
admin.site.register(Instructor)
admin.site.register(Participant)
admin.site.register(Module)
admin.site.register(CompletedEnrollment)
admin.site.register(CurrentEnrollment)
admin.site.register(Enrollment)
admin.site.register(SDPUser)
