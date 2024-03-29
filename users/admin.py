from django.contrib import admin
from .models import Course, Student

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_id","course_name","course_sem","course_year","course_total","course_status","all_students")

class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id","first_name","last_name","faculty","all_course")

admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)