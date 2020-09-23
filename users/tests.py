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

    # กรณีที่ล็อคอิน ผิดพลาด ต้องไม่สามารถเข้าสู่ระบบได้
    def test_login_1(self):
        """ check in test_login_1!! """
        response = self.client.post(self.login_url,{'username':'5555','password':'5555'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/login.html')
        self.assertEqual(response.context["message"],"Invalid Credential.")

    # กรณีที่ล็อคอินเป็น นักศึกษา ถูกต้อง ต้องสามารถเข้าสู่ระบบได้
    def test_login_2(self):
        """ check in test_login_2!! """
        user = User.objects.filter(email=self.user1.email).first()
        user.is_active=True
        user.save()
        response = self.client.post(self.login_url,{'username':user,'password':'12345'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

    # กรณีที่ล็อคอินเป็น แอดมิน ถูกต้อง ต้องสามารถเข้าสู่ระบบได้
    def test_login_3(self):
        """ check in test_login_3!! """
        user = User.objects.filter(email=self.user2.email).first()
        user.is_active=True
        user.save()
        response = self.client.post(self.login_url,{'username':user,'password':'1234'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/admin")

    # กรณีที่ล็อคอินถูกต้องและต้องการล็อคเอ้าท์ ต้องสามารถออกจากระบบได้
    def test_logout(self):
        """ check in test_logout!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

    # กรณีที่ไม่ได้ล็อคอิน ไม่สามารถเข้าถึงหน้า index ได้
    def test_index_1(self):
        """ check in test_index_1!! """
        response = self.client.post(self.index_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเป็นนักศึกษาถูกต้อง สามารถเข้าถึงหน้า  index ของนักศึกษาได้
    def test_index_2(self):
        """ check in test_index_2!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/index.html')
        self.assertEqual(response.context["courses"].count(),4)
        self.assertEqual(response.context["student"],self.s1)

    # กรณีที่ล็อคอินเป็นนักศึกษาสามารถเข้าถึงหน้า quota ได้
    def test_quota_1(self):
        """ check in test_quota_1!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.quota_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/quota.html')
        self.assertEqual(response.context["courses"].count(),0)
        self.assertEqual(response.context["student"],self.s1)

    # กรณีที่ไม่ได้ล็อคอิน ไม่สามารถเข้าถึงหน้า quota ได้
    def test_quota_2(self):
        """ check in test_quota_2!! """
        response = self.client.post(self.quota_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเป็นแอดมิน ไม่สามารถเข้าถึงหน้า quota ได้
    def test_quota_3(self):
        """ check in test_quota_3!! """
        self.client.force_login(self.user2)
        response = self.client.post(self.quota_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/admin")

    # กรณีที่ไม่ได้ล็อคอิน ไม่สามารถเข้าถึงหน้า index ของแอดมินได้
    def test_admin_1(self):
        """ check in test_admin_1!! """
        response = self.client.post(self.admin_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเป็นนักศึกษา ไม่สามารถเข้าถึงหน้า index ของแอดมินได้
    def test_admin_2(self):
        """ check in test_admin_2!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.admin_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

    # กรณีที่ล็อคอินเป็นadmin สามารถเข้าหน้า admin ได้
    def test_admin_3(self):
        """ check in test_admin_3!! """
        self.client.force_login(self.user2)
        response = self.client.post(self.admin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/admin.html')
        self.assertEqual(len(response.context["courses"]),4)

    # กรณีที่ไม่ได้ล็อคอิน ไม่สามารถเข้าถึงหน้า detail ของแอดมินได้
    def test_detail_1(self):
        """ check in test_detail_1!! """
        response = self.client.post(self.detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเป็นนักศึกษา ไม่สามารถเข้าถึงหน้า detail ของแอดมินได้
    def test_detail_2(self):
        """ check in test_detail_2!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.detail_url,)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

    # กรณีที่ล็อคอินเป็นแอดมิน เข้าถึงหน้า detail ของแอดมินได้
    def test_detail_3(self):
        """ check in test_detail_3!!!! """
        self.client.force_login(self.user2)
        response = self.client.post(self.detail_url,{'detail':'CN001',})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/detail.html')
        self.assertEqual(response.context["course"],self.c1)
        self.assertEqual(response.context["students"].count(),0)

    # กรณีที่ไม่ได้ล็อคอิน ไม่สามารถใช้แทปการค้นหาของแอดมินได้
    def test_search_admin_1(self):
        """ check in test_search_admin_1!! """
        response = self.client.post(self.search_admin_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเป็นนักศึกษา ไม่สามารถใช้แทปการค้นหาของแอดมินได้
    def test_search_admin_2(self):
        """ check in test_search_admin_2!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.search_admin_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

    # กรณีที่ที่นั่งว่าง ต้องสามารถกดขอโควต้าได้
    def test_add_quota_1(self):
        """ check in test_add_quota_1!! """
        s = Student.objects.get(student_id="6010610001")
        c = Course.objects.get(course_id="CN002")
        count = Student.objects.filter(course=c).count()
        if c not in s.course.all() and (count < int(c.course_total)) and c.course_status=="open":
            s.course.add(c)
        self.assertEqual(s.course.count(), 1)

    # กรณีที่ที่นั่งไม่ว่าง ต้องไม่สามารถกดขอโควต้าได้
    def test_add_quota_2(self):
        """ check in test_add_quota_2 """
        ss1 = Student.objects.get(student_id="6010610001")
        ss2 = Student.objects.get(student_id="6010610002")
        c = Course.objects.get(course_id="CN001")
        count = Student.objects.filter(course=c).count()
        if c not in ss1.course.all() and (count < int(c.course_total)) and c.course_status=="open":
            ss1.course.add(c)
        count = Student.objects.filter(course=c).count()
        if c not in ss2.course.all() and (count < int(c.course_total)) and c.course_status=="open":
            ss2.course.add(c)
        self.assertEqual(ss1.course.count(), 1)
        self.assertEqual(ss2.course.count(), 0)

    # กรณีที่ไม่ได้ล็อคอิน ไม่สามารถเข้าถึงการขอโควต้าได้
    def test_add_quota_3(self):
        """ check in test_add_quota_3!! """
        response = self.client.post(self.add_quota_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเป็นแอดมิน ต้องไม่สามารถขอโควต้าได้
    def test_add_quota_4(self):
        """ check in test_add_quota_4!! """
        self.client.force_login(self.user2)
        response = self.client.post(self.add_quota_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/admin")

    # กรณีที่นักศึกษาต้องการยกเลิกการขอโควต้า ต้องมีรายวิชานั้นอยู่ในการขอโควต้า
    def test_remove_quota_1(self):
        """ check in test_remove_quota_1!! """
        s = Student.objects.get(student_id="6010610001")
        c = Course.objects.get(course_id="CN001")
        s.course.add(c)
        if c in s.course.all() :
            s.course.remove(c)
        self.assertEqual(s.course.count(), 0)

    # กรณีที่ไม่ได้ล็อคอิน ไม่สามารถลบการขอโควต้าได้
    def test_remove_quota_2(self):
        """ check in test_remove_quota_2!! """
        response = self.client.post(self.remove_quota_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเป็นแอดมิน ไม่สามารถลบการขอโควต้าของนักศึกษาได้
    def test_remove_quota_3(self):
        """ check in test_search_admin_3!! """
        self.client.force_login(self.user2)
        response = self.client.post(self.remove_quota_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/admin")

    # สามารถค้นหาวิชาในระบบด้วยตัวอักษรพิมพ์ใหญ่
    def test_search_1(self):
        """ check in test_search_1!! """
        word = "CN"
        course1 = Course.objects.filter(course_id__contains=word.upper(), course_status="open")
        self.assertEqual(course1.count(), 2)

    # สามารถค้นหาวิชาในระบบด้วยเลขอาราบิก
    def test_search_2(self):
        """ check in test_search_2 """
        word = "001"
        course2 = Course.objects.filter(course_id__contains=word.upper(), course_status="open")
        self.assertEqual(course2.count(), 1)

    # กรณีที่ค้นหารายวิชาที่ไม่มีในระบบ ต้องไม่พบรายวิชานั้น
    def test_search_3(self):
        """ check in test_search_3 """
        word = "AT"
        course3 = Course.objects.filter(course_id__contains=word.upper(), course_status="open")
        self.assertEqual(course3.count(), 0)

    # สามารถค้นหาวิชาในระบบด้วยตัวอักษรพิมพ์เล็ก
    def test_search_4(self):
        """ check in test_search_4 """
        word = "cn"
        course4 = Course.objects.filter(course_id__contains=word.upper(), course_status="open")
        self.assertEqual(course4.count(), 2)

    # สามารถค้นหาวิชาในระบบด้วยตัวอักษรพิมพ์ใหญ่ผสมตัวอักษรพิมพ์เล็ก
    def test_search_5(self):
        """ check in test_search_5 """
        word = "cN"
        course5 = Course.objects.filter(course_id__contains=word.upper(), course_status="open")
        self.assertEqual(course5.count(), 2)

    # กรณีที่ไม่ได้ล็อคอิน ไม่สามารถใช้แทปการค้นหาของนักศึกษาได้
    def test_search_6(self):
        """ check in test_search_6!! """
        response = self.client.post(self.search_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเป็นแอดมิน ไม่สามารถใช้แทปการค้นหาของนักศึกษาได้
    def test_search_7(self):
        """ check in test_search_7!! """
        self.client.force_login(self.user2)
        response = self.client.post(self.search_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/admin")