from django.contrib import admin

# Register your models here.
from .courseModels import Course, Category, ImageComponent, TextComponent, FileComponent
from .courseModels import Module, CompletedEnrollment, CurrentEnrollment, VideoComponent
from .userModels import HR, Administrator, Instructor, Participant

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
admin.site.register(HR)
admin.site.register(VideoComponent)
