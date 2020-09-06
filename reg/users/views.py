from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Course, Student

# Create your views here.
def index(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if not request.user.is_staff :
            courses = Course.objects.all()
            return render(request, "users/index.html", {
                 "courses" : courses
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
            "message" : "Invalid Credential."
        })
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message" : "Logged out."
    })

def search(request):
    if request.method == "POST" :
        course_id = request.POST["course_id"].upper()
        courses = Course.objects.filter(course_id=course_id)
    return render(request, "users/index.html",{
            "courses" : courses
        })

def quota(request):
    if not request.user.is_staff :
        # print(user.member.all())
        student = Student.objects.get(first_name=request.user.first_name)
        return render(request, "users/quota.html", {
            "courses" : student.course.all()
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
                student = Student.objects.get(first_name=request.user.first_name)
                student.course.add(course)
                message = "Successful Quota Request."
            else :
                message = "Quota Request was Full."
    courses = Course.objects.all()
    return render(request, "users/index.html",{
        "message" : message,
        "courses" : courses
    })

def remove_quota(request) :
    if request.method == "POST" :
        course = Course.objects.get(course_id=request.POST["remove"])
        student = Student.objects.get(first_name=request.user.first_name)
        student.course.remove(course)
    courses = Course.objects.all()
    return render(request, "users/index.html",{
        "message" : "Successful Remove Quota Request.",
        "courses" : courses
    })

def admin(request) :
    courses = Course.objects.all()
    count = []
    for course in courses :
        cnt = Student.objects.filter(course=course).count()
        count.append(cnt)
    return render(request, "users/admin.html", {
        "courses" : zip(courses,count)
    })

def detail(request) :
    if request.method == "POST" :
        course = Course.objects.get(course_id=request.POST["detail"])
        students = Student.objects.filter(course=course)
        return render(request, "users/detail.html", {
            "course" : course,
            "students" : students
        })