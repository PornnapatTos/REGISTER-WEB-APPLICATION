from django.db import models
from django.utils.html import format_html
# from django.contrib.auth.models import User
# Create your models here.
class Course(models.Model):
    status = [
        ('open','Open'),
        ('close', 'Close'),
    ]
    course_id = models.CharField(max_length=5)
    course_name = models.CharField(max_length=64)
    course_sem = models.CharField(max_length=1)
    course_year = models.CharField(max_length=4)
    course_total = models.CharField(max_length=64)
    course_status = models.CharField(max_length=5, choices=status)

    def __str__(self) :
        return f"{self.course_id} : {self.course_name} {self.course_sem}/{self.course_year}"

    def all_students(self):
        course = Course.objects.get(course_id=self.course_id)
        student = Student.objects.filter(course=course)
        return format_html("<br />".join([s.first_name+" "+s.last_name for s in student]))

class Student(models.Model):
    student_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    course = models.ManyToManyField(Course , blank=True , related_name="students")
    faculty = models.CharField(max_length=64)
    def __str__(self) :
        return f"{self.student_id} : {self.first_name} {self.last_name} {self.faculty}"

    def all_course(self):
        return format_html("<br />".join([c.course_id for c in self.course.all()]))

