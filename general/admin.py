from django.contrib import admin

# Register your models here.
from .courseModels import *
from .userModels import HR,Administrator,Instructor,Participant

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(ImageComponent)
admin.site.register(TextComponent)
admin.site.register(FileComponent)
admin.site.register(Instructor)
admin.site.register(Participant)
admin.site.register(Module)
admin.site.register(CompletedEnrollment)
admin.site.register(CurrentEnrollment)
admin.site.register(Administrator)