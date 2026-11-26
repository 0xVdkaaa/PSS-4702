from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from .models import Course, CourseMember, CourseContent, Enrollment


class CourseModelTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create(username='teacher1')
        self.course = Course.objects.create(
            name="Pemrograman Django",
            description="Belajar Django",
            price=150000,
            teacher=self.teacher
        )

    def test_course_creation(self):
        course = Course.objects.get(name="Pemrograman Django")
        self.assertEqual(course.price, 150000)
        self.assertEqual(course.teacher.username, 'teacher1')
        self.assertEqual(str(course), course.name + " : " + str(course.price))


class CourseMemberModelTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create(username='teacher1')
        self.student = User.objects.create(username='student1')
        self.course = Course.objects.create(
            name="Pemrograman Django", teacher=self.teacher)

    def test_course_member_creation(self):
        member = CourseMember.objects.create(
            course_id=self.course, user_id=self.student, roles='std')
        self.assertEqual(member.user_id.username, 'student1')
        self.assertEqual(member.roles, 'std')


class CourseContentModelTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create(username='teacher1')
        self.course = Course.objects.create(
            name="Pemrograman Django", teacher=self.teacher)

    def test_course_content_creation(self):
        content = CourseContent.objects.create(
            name="Pengenalan Django",
            course_id=self.course,
            description="Materi dasar tentang Django"
        )
        self.assertEqual(content.course_id.name, "Pemrograman Django")
        self.assertEqual(content.name, "Pengenalan Django")
        self.assertEqual(str(content),
                         '[' + str(content.course_id) + '] ' + content.name)


class CourseQueryTest(TestCase):
    def setUp(self):
        self.teacher1 = User.objects.create(username='teacher1')
        self.teacher2 = User.objects.create(username='teacher2')
        Course.objects.create(name="Django", teacher=self.teacher1)
        Course.objects.create(name="Flask", teacher=self.teacher2)

    def test_course_retrieval_by_teacher(self):
        courses = Course.objects.filter(teacher=self.teacher1)
        self.assertEqual(courses.count(), 1)
        self.assertEqual(courses.first().name, "Django")


class CourseValidationTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create(username='teacher1')

    def test_invalid_price(self):
        # Course dengan harga negatif tetap tersimpan (belum ada validasi harga)
        course = Course(
            name="Pemrograman Django",
            description="Belajar Django",
            price=-10000,
            teacher=self.teacher
        )
        course.save()
        retrieved_course = Course.objects.get(pk=course.pk)
        self.assertEqual(retrieved_course.price, -10000)
        print("Test passed: Course allows negative prices")

    def test_empty_name(self):
        course = Course(
            name="",
            description="Belajar Django",
            price=100000,
            teacher=self.teacher
        )
        with self.assertRaises(ValidationError):
            course.full_clean()


class CourseFilteringTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create(username='teacher1')
        Course.objects.create(name="Kursus 1", price=100000,
                              teacher=self.teacher)
        Course.objects.create(name="Kursus 2", price=200000,
                              teacher=self.teacher)
        Course.objects.create(name="Kursus 3", price=300000,
                              teacher=self.teacher)

    def test_filter_courses_by_price(self):
        affordable_courses = Course.objects.filter(price__lt=200000)
        self.assertEqual(affordable_courses.count(), 1)
        self.assertEqual(affordable_courses.first().name, "Kursus 1")


class EnrollmentTestCase(TestCase):
    def setUp(self):
        self.teacher = User.objects.create(username='teacher1')
        self.student = User.objects.create(username='student1')
        self.course = Course.objects.create(
            name="Pemrograman Python",
            description="Kursus Python tingkat dasar",
            price=50000,
            teacher=self.teacher
        )

    def test_enrollment_success(self):
        enrollment = Enrollment.objects.create(
            course=self.course,
            student=self.student,
            status='paid'
        )
        self.assertEqual(enrollment.course.name, "Pemrograman Python")
        self.assertEqual(enrollment.student.username, "student1")
        self.assertEqual(enrollment.status, 'paid')

    def test_duplicate_enrollment(self):
        Enrollment.objects.create(
            course=self.course,
            student=self.student,
            status='paid'
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Enrollment.objects.create(
                    course=self.course,
                    student=self.student,
                    status='pending'
                )

    def test_course_full(self):
        # Kuota course diatur menjadi 1 siswa
        self.course.max_students = 1
        self.course.save()
        enrollment1 = Enrollment.objects.create(
            course=self.course,
            student=self.student,
            status='paid'
        )
        self.assertEqual(enrollment1.student, self.student)
        student2 = User.objects.create(username='student2')
        enrollment2 = Enrollment(
            course=self.course,
            student=student2,
            status='paid'
        )
        try:
            enrollment2.save()
            self.fail("Should raise an exception when course is full")
        except Exception:
            pass
