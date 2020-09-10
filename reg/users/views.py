from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Course, Student
from django.contrib import admin as admin_r

# Create your views here.
def index(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if not request.user.is_staff :
            student = Student.objects.get(first_name=request.user.first_name)
            courses = Course.objects.all()
            return render(request, "users/index.html", {
                "courses" : courses,
                "student" : student
            })
        else :
            return HttpResponseRedirect(reverse("admin"))

def login_view(request):
    if request.method == "POST" :
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request , user)
            if not user.is_staff :
                return HttpResponseRedirect(reverse("index"))
            else :
                return HttpResponseRedirect(reverse("admin"))
        return render(request, "users/login.html", {
            "message":"Invalid Credential."
        })
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message":"Logged out."
    })

def search(request):
    if request.method == "POST" :
        course_id = request.POST["course_id"].upper()
        if course_id == "*" :
            courses = Course.objects.all()
            print(courses)
        else :
            courses = Course.objects.filter(course_id__contains=course_id)
            if len(courses) == 1 :
                cc = [course for course in courses]
                if cc[0].course_status == "close" :
                    if not request.user.is_staff :
                        courses = ""
        student = Student.objects.get(first_name=request.user.first_name)
    return render(request, "users/index.html",{
            "courses" : courses,
            "student" : student
        })

def quota(request):
    if not request.user.is_staff :
        # print(user.member.all())
        student = Student.objects.get(first_name=request.user.first_name)
        return render(request, "users/quota.html", {
            "courses" : student.course.all(),
            "student" : student
        })
    else :
        return HttpResponseRedirect(reverse("admin"))

def add_quota(request) :
    if request.method == "POST" :
        course = Course.objects.get(course_id=request.POST["add"])
        student = Student.objects.get(first_name=request.user.first_name)
        if course in student.course.all() :
            message = "you are already add this course."
        else :
            count = Student.objects.filter(course=course).count()
            if count < int(course.course_total) :
                # student = Student.objects.get(first_name=request.user.first_name)
                student.course.add(course)
                message = "Successful Quota Request."
            else :
                message = "Quota Request was Full."
    courses = Course.objects.all()
    return render(request, "users/index.html",{
        "message" : message,
        "courses" : courses,
        "student" : student
    })

def remove_quota(request) :
    student = Student.objects.get(first_name=request.user.first_name)
    if request.method == "POST" :
        course = Course.objects.get(course_id=request.POST["remove"])
        student.course.remove(course)
    return render(request, "users/quota.html",{
        "message" : "Successful Remove Quota Request.",
        "courses" : student.course.all(),
        "student" : student
    })

def admin(request) :
    if request.user.is_staff :
        courses = Course.objects.all()
        count = []
        for course in courses :
            cnt = Student.objects.filter(course=course).count()
            count.append(cnt)
        return render(request, "users/admin.html", {
            "courses" : zip(courses,count)
        })
    else :
        return HttpResponseRedirect(reverse("index"))

def detail(request) :
    if request.method == "POST" :
        course = Course.objects.get(course_id=request.POST["detail"])
        students = Student.objects.filter(course=course)
        return render(request, "users/detail.html", {
            "course" : course,
            "students" : students
        })

def search_admin(request):
    if request.method == "POST" :
        course_id = request.POST["course_id"].upper()
        if course_id == "*" :
            courses = Course.objects.all()
            print(courses)
        else :
            courses = Course.objects.filter(course_id__contains=course_id)
            print(len(courses))
        count = []
        for course in courses :
            cnt = Student.objects.filter(course=course).count()
            count.append(cnt)
    return render(request, "users/search_admin.html",{
            "courses" : zip(courses,count),
            "total_course" : len(courses)
        })


