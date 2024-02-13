from django.contrib import admin

from .models import AdvUser, Machine, Spare, Course, Student

admin.site.register(AdvUser)
admin.site.register(Machine)
admin.site.register(Spare)
admin.site.register(Course)
admin.site.register(Student)