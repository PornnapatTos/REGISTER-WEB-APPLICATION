from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
from .models import Course, Student
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
# Create your tests here.

class TestView(TestCase):

    def setUp(self):

        # create student
        self.s1 = Student.objects.create(student_id="6010610001",first_name="student",last_name="one",faculty="Engineering")
        self.s2 = Student.objects.create(student_id="6010610002",first_name="student",last_name="two",faculty="Engineering")

        # create course
        self.c1 = Course.objects.create(course_id="CN001",course_name="subject1",course_sem="1",course_year="2563",course_total="1",course_status="open")
        self.c2 = Course.objects.create(course_id="CN002",course_name="subject2",course_sem="1",course_year="2563",course_total="2",course_status="open")
        self.c3 = Course.objects.create(course_id="CN003",course_name="subject3",course_sem="2",course_year="2563",course_total="1",course_status="close")
        self.c4 = Course.objects.create(course_id="CN004",course_name="subject4",course_sem="2",course_year="2563",course_total="2",course_status="close")

        # create user
        self.user1 = User.objects.create_user(username='6010610001', password='12345', email='6010610001@reg.com')
        self.user2 = User.objects.create_superuser(username='admin', password='1234', email='admin@reg.com')

        # path url
        self.index_url = reverse('index')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.search_url = reverse('search')
        self.quota_url = reverse('quota')
        self.add_quota_url = reverse('add_quota')
        self.remove_quota_url = reverse('remove_quota')
        self.admin_url = reverse('admin')
        self.detail_url = reverse('detail')
        self.search_admin_url = reverse('search_admin')

        # Client
        self.client = Client()

    def redirect(self , res):
        return dict(res.items())['Location']

    def test_login_1(self):
        """ check in test_login_1!! """
        response = self.client.post(self.login_url,{'username':'5555','password':'5555'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/login.html')
        self.assertEqual(response.context["message"],"Invalid Credential.")

    def test_login_2(self):
        """ check in test_login_2!! """
        user = User.objects.filter(email=self.user1.email).first()
        user.is_active=True
        user.save()
        response = self.client.post(self.login_url,{'username':user,'password':'12345'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

    def test_login_3(self):
        """ check in test_login_3!! """
        user = User.objects.filter(email=self.user2.email).first()
        user.is_active=True
        user.save()
        response = self.client.post(self.login_url,{'username':user,'password':'1234'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/admin")

    def test_logout(self):
        """ check in test_logout!! """
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")
    def test_index_1(self):
        """ check in test_index_1!! """
        response = self.client.post(self.index_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    def test_index_2(self):
        """ check in test_index_2!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/index.html')
        self.assertEqual(response.context["courses"].count(),4)
        self.assertEqual(response.context["student"],self.s1)

    def test_index_3(self):
        """ check in test_index_3!! """
        self.client.force_login(self.user2)
        response = self.client.post(self.index_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/admin")

    def test_quota_1(self):
        """ check in test_quota_1!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.quota_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/quota.html')
        self.assertEqual(response.context["courses"].count(),0)
        self.assertEqual(response.context["student"],self.s1)

    def test_quota_2(self):
        """ check in test_quota_2!! """
        response = self.client.post(self.quota_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    def test_quota_3(self):
        """ check in test_quota_3!! """
        self.client.force_login(self.user2)
        response = self.client.post(self.quota_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/admin")

    def test_admin_1(self):
        """ check in test_admin_1!! """
        response = self.client.post(self.admin_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    def test_admin_2(self):
        """ check in test_admin_2!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.admin_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

    def test_admin_3(self):
        """ check in test_admin_3!! """
        self.client.force_login(self.user2)
        response = self.client.post(self.admin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/admin.html')
        self.assertEqual(len(response.context["courses"]),4)