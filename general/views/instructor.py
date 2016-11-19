from django.shortcuts import render,redirect,render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from ..courseModels import Category,Course
from ..userModels import Instructor
from ..forms import ComponentForm
from . import authenticate
from ..exceptions import NameDuplication

@login_required
def InstructorIndex(request,instructorID):
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor = Instructor.getFromUser(request.user)
        developingCourses = instructor.getDevelopingCourses()
        openCourses = instructor.getOpenedCourses()
        if request.method=="POST":
            courseID=int(request.POST.get("id"))
            try:
                instructor.deleteCourse(Course.getByID(courseID))
            except Exception:
                result=False
            else:
                result=True
            return JsonResponse({"result":result})
        return render(request,"general/instructorIndex.html",{'developingCourses':developingCourses,'openCourses':openCourses})
    return redirect("myLogout")

@login_required
def newCourse(request,instructorID):
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        if request.method == "POST":
            name = request.POST.get('name')
            description = request.POST.get("description")
            categoryID = request.POST.get("categoryID")
            category = Category.getByID(categoryID)
            instructor = Instructor.getFromUser(request.user)
            try:
                course = instructor.createCourse(name,description,category)
            except NameDuplication:
                result = False
                newID=-2
            except Exception as e:
                result = False
                newID=-1
            else:
                result = True
                newID=course.id
            return JsonResponse({'result':result,'newCourseID':newID})
        else:
            categories = Category.getAllCategories()
            return render(request, "general/newCourse.html",{'categories':categories})
    return redirect("myLogout")

@login_required
def coursePage(request,instructorID,courseID):
    courseID=int(courseID)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if request.method=="POST":
                action=request.POST.get("action")
                if action=="OPEN":
                    try:
                        instructor.openCourse(course)
                    except Exception:
                        result=False
                    else:
                        result=True
                    return JsonResponse({"result":result})
                elif action=="DELETE":
                    moduleIndex=int(request.POST.get("index"))
                    module=course.getModuleByIndex(moduleIndex)
                    try:
                        course.deleteModule(module)
                    except Exception:
                        result=False
                    else:
                        result=True
                    return JsonResponse({"result":result})
            if request.method=="GET":
                modules = course.getSortedModules()
                return render(request,"general/developCourse.html",{'course':course,'modules':modules,"isOpen":course.isOpen()})
        else:
            print(courseID,"not in ",list(map((lambda x:x.id),instructor.getAllCourses())))
    return redirect("myLogout")


@login_required
def changeModuleOrder(request,instructorID,courseID):
    instructorID=int(instructorID)
    courseID=int(courseID)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if request.method=="POST":
                originIndex = int(request.POST.get("originIndex"))
                newIndex = int(request.POST.get("newIndex"))
                try:
                    course.updateIndex(originIndex,newIndex)
                except Exception:
                    result=False
                else:
                    result=True
                modules = course.getSortedModules()
                data=render_to_string("general/ajax/modules.html",{"modules":modules})
                return JsonResponse({"result":result,"data":data})
            else:
                return HttpResponse(status=404)
    return redirect("myLogout")


@login_required
def editCourse(request,instructorID,courseID):
    courseID=int(courseID)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if request.method=="POST":
                name=request.POST.get("name")
                description = request.POST.get("description")
                categoryID = request.POST.get("categoryID")
                category = Category.getByID(categoryID)
                try:
                    instructor.modifyCourse(course,name,description,category)
                except NameDuplication:
                    errno=-2
                except Exception as err:
                    print(err)
                    errno=-1
                else:
                    errno=0
                return JsonResponse({"result":errno})
            else:
                categories = Category.getAllCategories()
                return render(request,"general/editCourse.html",{"course":course, "categories":categories})
    return redirect("myLogout")

@login_required
def newModule(request,instructorID,courseID):
    courseID=int(courseID)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course =instructor.getCourseByID(courseID)
            if request.method == "POST":
                name = request.POST.get('name')
                description = request.POST.get('description')
                index = int(request.POST.get('index'))
                try:
                    module = course.createModule(name,description,index)
                except NameDuplication:
                    newIndex=-2
                    result=False
                except Exception:
                    newIndex=-1
                    result=False
                else:
                    newIndex=module.index
                    result=True
                return JsonResponse({'result':result,"newModuleIndex":newIndex})
            elif request.method == "GET":
                return render(request, "general/newModule.html")
    return redirect("myLogout")

@login_required
def modulePage(request,instructorID,courseID,moduleIndex):
    courseID=int(courseID)
    moduleIndex=int(moduleIndex)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course=instructor.getCourseByID(courseID)
            if course.hasModule(moduleIndex):
                module=course.getModuleByIndex(moduleIndex)                
                if request.method=="POST":
                    componentIndex=int(request.POST.get("index"))
                    component=module.getComponentByIndex(componentIndex)
                    try:
                        module.deleteComponent(component)
                    except Exception:
                        result=False
                    else:
                        result=True
                    return JsonResponse({"result":result})
                else:
                    components = module.getSortedComponents()
                    return render(request,"general/modulePage.html",{'course':course,'module':module,'components':components,"isOpen":course.isOpen()})
    return redirect("myLogout")

@login_required
def editModule(request,instructorID,courseID,moduleIndex):
    courseID=int(courseID)
    moduleIndex=int(moduleIndex)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if course.hasModule(moduleIndex):
                module=course.getModuleByIndex(moduleIndex)
                if request.method=="POST":
                    name=request.POST.get("name")
                    description = request.POST.get("description")
                    try:
                        course.modifyModule(module,name,description)
                    except NameDuplication:
                        errno=-2
                    except Exception as err:
                        print(err)
                        errno=-1
                    else:
                        errno=0
                    return JsonResponse({"result":errno})
                else:
                    return render(request,"general/editModule.html",{"module":module})
    return redirect("myLogout")



@login_required
def newComponent(request,instructorID,courseID,moduleIndex):
    courseID=int(courseID)
    moduleIndex=int(moduleIndex)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course=instructor.getCourseByID(courseID)
            if course.hasModule(moduleIndex):
                module=course.getModuleByIndex(moduleIndex)
                if request.method =="POST":
                    typeName = request.POST.get('typeName')
                    index = int(request.POST.get('index'))
                    if typeName!="TEXT":
                        form = ComponentForm(request.POST,request.FILES)
                        if form.is_valid():
                            try:
                                component = module.createComponent(typeName,index,request.FILES['file'])
                            except Exception as e:
                                print(e)
                                result=False
                            else:
                                result=True
                            return JsonResponse({'result':result})
                    else:
                        text = request.POST.get("text")
                        try:
                            component = module.createComponent("TEXT",index,text)
                        except Exception as e:
                            print(e)
                            result=False
                        else:
                            result=True
                        return JsonResponse({"result":result})
                else:
                    form = ComponentForm()
                    return render(request,"general/newComponent.html",{"form":form})
    return HttpResponse(status=404)


@login_required
def changeComponentOrder(request,instructorID,courseID,moduleIndex):
    instructorID=int(instructorID)
    courseID=int(courseID)
    moduleIndex=int(moduleIndex)
    if authenticate.roleCheck(request.user,"Instructor",instructorID):
        instructor=Instructor.getFromUser(request.user)
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if course.hasModule(moduleIndex):
                module=course.getModuleByIndex(moduleIndex)
                if request.method=="POST":
                    originIndex = int(request.POST.get("originIndex"))
                    newIndex = int(request.POST.get("newIndex"))
                    try:
                        module.updateIndex(originIndex,newIndex)
                    except Exception:
                        result=False
                    else:
                        result=True
                    components = module.getSortedComponents()
                    data=render_to_string("general/ajax/components.html",{"components":components})
                    return JsonResponse({"result":result,"data":data})
                else:
                    return HttpResponse(status=404)
    return redirect("myLogout")
