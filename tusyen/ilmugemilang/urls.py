from django.urls import path 
from . import views 

urlpatterns = [
    path("",views.index,name="index"),
    path("usersignup/",views.usersignup,name="usersignup"),
    path("userlogin/",views.userlogin,name="userlogin"),
    path("teachersignup/",views.teachersignup,name="teachersignup"),
    path("teacherlogin/",views.teacherlogin,name="teacherlogin"),
    path("adminlogin/",views.adminlogin,name="adminlogin"),
    path("logout/",views.user_logout,name="logout"),
    path("mainpage/",views.mainpage,name="mainpage"),
    path("mainpage2/",views.mainpage2,name="mainpage2"),

    #user 
    path("register/",views.register,name="register"),
    path("register/viewregister/<str:studname>/",views.viewregister,name="viewregister"),
    path("viewregister/updateregister/<str:studname>/",views.updateregister,name="updateregister"),
    path("course/",views.program,name="course"),
    path("fee/",views.fee,name="fee"),
    path("contact/",views.contact,name="contact"),


    #TEACHER
    path("teacher/",views.teacher,name="teacher"),
    path("attendance/<str:class_id>/",views.attendance_form,name="attendance_form"),
    path("viewattendance/<str:class_id>/",views.viewattendance,name="viewattendance"),
    

    #ADMIN
    path("admin/",views.admin,name="admin"),
    path("managestudent/",views.managestudent,name="managestudent"),
    path("viewstudent/updatestudent/<str:student_id>/", views.updatestudent, name="updatestudent"),
    path("viewstudent/deletestudent/<str:studname>/", views.deletestudent, name="deletestudent"),
    path("manageclass/",views.manageclass,name="manageclass"),
    path('managepayment/', views.managepayment, name='managepayment'),
    path('viewpayment/', views.viewpayment, name='viewpayment'),
]