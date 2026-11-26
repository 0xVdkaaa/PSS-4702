from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import Course, CourseMember, CourseContent, Comment


def core(request):
    return render(request, 'core.html')


# ---------- Query dasar: insert ----------
def insert_user(request):
    user = User.objects.create_user(
        username='mahasiswa_baru', password='12345',
        email='mahasiswa_baru@gmail.com')
    return HttpResponse(f"User berhasil dibuat: {user.username} (id={user.id})")


def insert_course(request):
    teacher = User.objects.first()
    course = Course.objects.create(
        name='Pemrograman Sisi Server', description='Belajar backend Django',
        price=150000, teacher=teacher)
    return HttpResponse(f"Course berhasil dibuat: {course.name} (id={course.id})")


# ---------- Query dasar: read ----------
def user_list(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


def user_json(request):
    users = User.objects.all().values('id', 'username', 'email')
    return JsonResponse(list(users), safe=False)


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_detail.html', {'user': user})


def search_user(request):
    keyword = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=keyword)
    return render(request, 'users.html',
                  {'users': users, 'keyword': keyword})


# ---------- Query dasar: update & delete ----------
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.email = 'email_baru@gmail.com'
    user.save()
    return HttpResponse(f"Email user {user.username} diubah menjadi {user.email}")


def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    username = user.username
    user.delete()
    return HttpResponse(f"User {username} berhasil dihapus")


def delete_all_courses(request):
    jumlah, _ = Course.objects.all().delete()
    return HttpResponse(f"Semua course berhasil dihapus ({jumlah} baris)")


def delete_users_except(request, pk):
    jumlah, _ = User.objects.exclude(pk=pk).delete()
    return HttpResponse(f"Semua user kecuali id={pk} dihapus ({jumlah} baris)")


# ---------- Query relational ----------
def all_courses(request):
    courses = Course.objects.all()
    result = []
    for course in courses:
        record = {
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'price': course.price,
            'teacher': {
                'id': course.teacher.id,
                'username': course.teacher.username,
                'email': course.teacher.email,
            },
            'jumlah_member': course.coursemember_set.count(),
        }
        result.append(record)
    return JsonResponse(result, safe=False)


# ---------- Statistik dengan optimasi ORM (annotate + select_related) ----------
from django.db.models import Count


def course_statistic(request):
    courses = Course.objects.select_related('teacher').annotate(
        jumlah_member=Count('coursemember', distinct=True),
        jumlah_konten=Count('coursecontent', distinct=True),
        jumlah_komentar=Count('coursecontent__comment', distinct=True),
    )
    return render(request, 'course_statistic.html', {'courses': courses})


def user_statistic(request):
    users = User.objects.annotate(
        jumlah_course_diikuti=Count('coursemember', distinct=True),
        jumlah_komentar=Count('coursemember__comment', distinct=True),
    )
    return render(request, 'user_statistic.html', {'users': users})


# ---------- Halaman HTML: daftar course dengan search, sorting, pagination ----------
from django.core.paginator import Paginator


def course_page(request):
    qs = Course.objects.select_related('teacher').all()
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(name__icontains=q)
    sort = request.GET.get('sort', 'id')
    if sort in ("price", "-price", "name", "-name"):
        qs = qs.order_by(sort)
    paginator = Paginator(qs, 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'courses.html',
                  {'page_obj': page_obj, 'q': q, 'sort': sort})
