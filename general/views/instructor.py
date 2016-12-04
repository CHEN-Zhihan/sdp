from django.shortcuts import render, redirect, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..courseModels import Category, Course, ComponentAdapter
from ..userModels import Instructor, UserManager
from . import authenticate
from ..exceptions import NameDuplication, NoModuleException


@login_required
def InstructorIndex(request, instructorID):
    instructorID = int(instructorID)
    instructor = UserManager.getInstance().getFromUser(request.user, Instructor, instructorID)
    if instructor is not None:
        if request.method == "POST":
            courseID = int(request.POST.get("id"))
            try:
                Course.getByID(courseID).deleteSelf()
            except Exception as e:
                print(e)
                result = False
            else:
                result = True
            return JsonResponse({"result": result})
        else:
            developingCourses = instructor.getDevelopingCourses()
            openCourses = instructor.getOpenedCourses()
            return render(request, "general/instructorIndex.html", {'developingCourses': developingCourses,
                                                                    'openCourses': openCourses})
    return redirect("myLogout")


@login_required
def newCourse(request, instructorID):
    instructorID = int(instructorID)
    instructor = UserManager.getInstance().getFromUser(request.user, Instructor, instructorID)
    if instructor is not None:
        if request.method == "POST":
            name = request.POST.get('name')
            description = request.POST.get("description")
            categoryID = request.POST.get("categoryID")
            category = Category.getByID(categoryID)
            try:
                course = instructor.createCourse(name, description, category)
            except NameDuplication:
                result = False
                newID = -2
            except Exception as e:
                result = False
                newID = -1
            else:
                result = True
                newID = course.id
            return JsonResponse({'result': result, 'newCourseID': newID})
        else:
            categories = Category.getAllCategories()
            return render(request, "general/newCourse.html", {'categories': categories})
    return redirect("myLogout")


@login_required
def coursePage(request, instructorID, courseID):
    courseID = int(courseID)
    instructorID = int(instructorID)
    instructor = UserManager.getInstance().getFromUser(request.user, Instructor, instructorID)
    if instructor is not None:
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if request.method == "POST":
                action = request.POST.get("action")
                if action == "OPEN":
                    try:
                        course.openCourse()
                    except NoModuleException:
                        result = -2
                    except Exception as e:
                        print(e)
                        result = -1
                    else:
                        result = 0
                    return JsonResponse({"result": result})
                elif action == "DELETE":
                    moduleIndex = int(request.POST.get("index"))
                    module = course.getModuleByIndex(moduleIndex)
                    try:
                        course.deleteModule(module)
                    except Exception:
                        result = False
                    else:
                        result = True
                    return JsonResponse({"result": result})
            else:
                modules = course.getSortedModules()
                return render(request, "general/instructorCourse.html", {'course': course,
                                                                         'modules': modules,
                                                                         "isOpen": course.isOpen()})
        return HttpResponse(status=404)
    return redirect("myLogout")


@login_required
def changeModuleOrder(request, instructorID, courseID):
    instructorID = int(instructorID)
    courseID = int(courseID)
    instructor = UserManager.getInstance().getFromUser(request.user, Instructor, instructorID)
    if instructor is not None:
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if request.method == "POST":
                originIndex = int(request.POST.get("originIndex"))
                newIndex = int(request.POST.get("newIndex"))
                try:
                    course.updateIndex(originIndex, newIndex)
                except Exception:
                    result = False
                else:
                    result = True
                modules = course.getSortedModules()
                data = render_to_string("general/ajax/modules.html", {"modules": modules})
                return JsonResponse({"result": result, "data": data})
        return HttpResponse(status=404)
    return redirect("myLogout")


@login_required
def editCourse(request, instructorID, courseID):
    courseID = int(courseID)
    instructorID = int(instructorID)
    instructor = UserManager.getInstance().getFromUser(request.user, Instructor, instructorID)
    if instructor is not None:
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if not course.isOpen():
                if request.method == "POST":
                    name = request.POST.get("name")
                    description = request.POST.get("description")
                    categoryID = request.POST.get("categoryID")
                    category = Category.getByID(categoryID)
                    try:
                        course.updateInfo(name, category, description)
                    except NameDuplication:
                        errno = -2
                    except Exception as err:
                        print(err)
                        errno = -1
                    else:
                        errno = 0
                    return JsonResponse({"result": errno})
                else:
                    categories = Category.getAllCategories()
                    return render(request, "general/editCourse.html", {"course": course, "categories": categories})
        return HttpResponse(status=404)
    return redirect("myLogout")


@login_required
def newModule(request, instructorID, courseID):
    courseID = int(courseID)
    instructorID = int(instructorID)
    instructor = UserManager.getInstance().getFromUser(request.user, Instructor, instructorID)
    if instructor is not None:
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if request.method == "POST":
                name = request.POST.get('name')
                description = request.POST.get('description')
                try:
                    index = int(request.POST.get('index'))
                except ValueError:
                    return JsonResponse({'result': -1, "newModuleIndex": -1})
                try:
                    module = course.createModule(name, description, index)
                except NameDuplication:
                    newIndex = -2
                    result = False
                except Exception:
                    newIndex = -1
                    result = False
                else:
                    newIndex = module.index
                    result = True
                return JsonResponse({'result': result, "newModuleIndex": newIndex})
            else:
                return render(request, "general/newModule.html")
        return HttpResponse(status=404)
    return redirect("myLogout")


@login_required
def modulePage(request, instructorID, courseID, moduleIndex):
    courseID = int(courseID)
    moduleIndex = int(moduleIndex)
    instructorID = int(instructorID)
    instructor = UserManager.getInstance().getFromUser(request.user, Instructor, instructorID)
    if instructor is not None:
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if course.hasModule(moduleIndex):
                module = course.getModuleByIndex(moduleIndex)
                if request.method == "POST":
                    componentIndex = int(request.POST.get("index"))
                    component = module.getComponentByIndex(componentIndex)
                    try:
                        module.deleteComponent(component)
                    except Exception as e:
                        print(e)
                        result = False
                    else:
                        result = True
                    return JsonResponse({"result": result})
                else:
                    components = list(map(ComponentAdapter, module.getSortedComponents()))
                    print(list(map((lambda x: x.typeName), components)))
                    return render(request, "general/instructorModule.html", {'course': course,
                                                                             'module': module,
                                                                             'components': components,
                                                                             "isOpen": course.isOpen()})
        return HttpResponse(status=404)
    return redirect("myLogout")


@login_required
def editModule(request, instructorID, courseID, moduleIndex):
    courseID = int(courseID)
    moduleIndex = int(moduleIndex)
    instructorID = int(instructorID)
    instructor = UserManager.getInstance().getFromUser(request.user, Instructor, instructorID)
    if instructor is not None:
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if course.hasModule(moduleIndex) and not course.isOpen():
                module = course.getModuleByIndex(moduleIndex)
                if request.method == "POST":
                    name = request.POST.get("name")
                    description = request.POST.get("description")
                    try:
                        module.updateInfo(name, description)
                    except NameDuplication:
                        errno = -2
                    except Exception as err:
                        print(err)
                        errno = -1
                    else:
                        errno = 0
                    return JsonResponse({"result": errno})
                else:
                    return render(request, "general/editModule.html", {"module": module})
        return HttpResponse(status=404)
    return redirect("myLogout")


@login_required
def newComponent(request, instructorID, courseID, moduleIndex):
    courseID = int(courseID)
    moduleIndex = int(moduleIndex)
    instructorID = int(instructorID)
    instructor = UserManager.getInstance().getFromUser(request.user, Instructor, instructorID)
    if instructor is not None:
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if course.hasModule(moduleIndex):
                module = course.getModuleByIndex(moduleIndex)
                if request.method == "POST":
                    typeName = request.POST.get('typeName')
                    try:
                        index = int(request.POST.get('index'))
                    except ValueError:
                        return JsonResponse({"result": False})
                    if typeName == "FILE" or typeName == "IMAGE":
                        try:
                            component = module.createComponent(typeName, index, request.FILES['file'])
                        except Exception as e:
                            print(e)
                            result = False
                        else:
                            result = True
                        return JsonResponse({'result': result})
                    else:
                        text = request.POST.get("text")
                        try:
                            component = module.createComponent(typeName, index, text)
                        except Exception as e:
                            print(e)
                            result = False
                        else:
                            result = True
                        return JsonResponse({"result": result})
                else:
                    return render(request, "general/newComponent.html")
        return HttpResponse(status=404)
    return redirect("myLogout")


@login_required
def changeComponentOrder(request, instructorID, courseID, moduleIndex):
    instructorID = int(instructorID)
    courseID = int(courseID)
    moduleIndex = int(moduleIndex)
    instructor = UserManager.getInstance().getFromUser(request.user, Instructor, instructorID)
    if instructor is not None:
        if instructor.ownCourse(courseID):
            course = instructor.getCourseByID(courseID)
            if course.hasModule(moduleIndex):
                module = course.getModuleByIndex(moduleIndex)
                if request.method == "POST":
                    originIndex = int(request.POST.get("originIndex"))
                    newIndex = int(request.POST.get("newIndex"))
                    try:
                        module.updateIndex(originIndex, newIndex)
                    except Exception:
                        result = False
                    else:
                        result = True
                    components = list(map(ComponentAdapter, module.getSortedComponents()))
                    data = render_to_string("general/ajax/components.html", {"components": components})
                    return JsonResponse({"result": result, "data": data})
        return HttpResponse(status=404)
    return redirect("myLogout")
