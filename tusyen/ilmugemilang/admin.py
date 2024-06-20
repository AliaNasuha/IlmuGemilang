from django.contrib import admin
from .models import Student,Teacher,Contact,Class,AssignClass,Payment,Attendance

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Contact)
admin.site.register(Class)
admin.site.register(AssignClass)
admin.site.register(Payment)
admin.site.register(Attendance)