# Staff Development Platform
GitHub page: [SDP](https://github.com/CHEN-Zhihan/sdp)
What is it?
-----------
The Staff Development Platform (or SDP) serves as an educational plaform for course delivery
in the AB Credit staff development and continuing education programme. Courses are to be
prepared by instructors and to be taken by staff participating in the program through SDP.

Version
-------
Beta version 1.0 is to be released in mid-December.

Usage
-----
This project is developed using Python3 on Django. To start the server locally, run
```
pip3 install django
python3 manage.py runserver
```
and access [localhost:8000](localhost:8000).
### Database
A demonstration database is included. The superuser of the website is
```
username: admin
password: comp3297
```
The administrator of AB Credit staff is
```
username: Admin
password: comp3297
```
The instructor (at the same time a participant) is
```
username: zixuwang
password: comp3297
```
The HR is
```
username: changgao
password: comp3297
```
A participant is
```
username: jingwang
password: comp3297
```

### Participant
Currently enrolled and completed courses will be displayed on the home page of participant:

![participant home](/doc/screenshots/participantHome.png)

Participant can explore opened courses under different categories by selecting categories in the left navigation bar:

![participant browse courses](/doc/screenshots/participantBrowse.png)

![participant view course](/doc/screenshots/participantViewCourse.png)

In a course page, participant can view available modules:

![participant take course](/doc/screenshots/participantTakeCourse.png)

In a module page, participant can view relevant components:

![participant module](/doc/screenshots/participantModule.png)

Participant can only take one course at a time. Participant can drop a current enrollment at any time. Participant can retake a completed course.


### Instructor
Currently developing and opened courses will be displayed on the home page of instructor:

![instructor home](/doc/screenshots/instructorHome.png)

Instructor can create a course, edit its information, delete, and open a course.

In a developing course, instructor can create or delete a module, edit its information, and reorder modules.

In both developing and opened courses, instructor can add components to a module, and reorder the components.

Instructor can reorder modules and components by simply drag-and-drop:

![instructor reorder module](/doc/screenshots/instructorReorderModule.png)

![instructor reorder component](/doc/screenshots/instructorReorderComponent.png)


### Administrator
All users and courses will be displayed on the home page of administrator. Administrator can designate users as instructors:

![administrator home](/doc/screenshots/administratorHome.png)


### HR
All users will be displayed on the home page of HR:

![HR home](/doc/screenshots/HRHome.png)

Other functionalities of HR are not implemented in this release.


Known bugs and limitations
--------------------------
All features listed in Elaobration 1, Elaboration 2, and Construction has been implemented,
as well as those listed in change requests during these iterations. There are no significant
bugs in the current version.
