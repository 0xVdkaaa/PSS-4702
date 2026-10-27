from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Course

# Create your views here.
from django.http import HttpResponse

def core(request):
    return HttpResponse("Hello world!")

def users(request):
  myusers = User.objects.all().values()
  template = loader.get_template('all_users.html')
  context = {
    'myusers': myusers,
  }
  return HttpResponse(template.render(context, request))

# 1. Insert data User
def insert_user(request):
    user, created = User.objects.get_or_create(
        username="usertesting",
        defaults={"email": "usertest@email.com"}
    )

    if created:
        user.set_password("sanditesting")
        user.save()

    return JsonResponse({
        "message": "User berhasil ditambahkan" if created
                   else "User sudah tersedia",
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })


# 2. Insert data Course
def insert_course(request):
    teacher = get_object_or_404(User, pk=1)

    course = Course.objects.create(
        name="Pemrograman Python",
        description="Belajar dasar pemrograman Python",
        price=150000,
        teacher=teacher,
    )

    return JsonResponse({
        "message": "Course berhasil ditambahkan",
        "id": course.id,
        "name": course.name,
        "teacher": course.teacher.username,
    })


# 3. Select semua User, tampilkan dalam HTML
def user_list(request):
    users = User.objects.all().order_by("id")
    return render(request, "users.html", {"users": users})


# 4. Select semua User, tampilkan sebagai JSON
def user_json(request):
    users = User.objects.all().values(
        "id", "username", "email", "first_name", "last_name"
    )
    return JsonResponse(list(users), safe=False)


# 5. Select satu User berdasarkan ID, tampilkan dalam HTML
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, "user_detail.html", {"user": user})


# 6. Select User dengan kondisi WHERE
def search_user(request):
    username = request.GET.get("username", "")
    users = User.objects.filter(
        username__icontains=username
    ).order_by("id")

    return render(request, "users.html", {"users": users})


# 7. Update data User
@require_POST
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.email = request.POST.get("email", user.email)
    user.save()

    return JsonResponse({
        "message": "User berhasil diupdate",
        "id": user.id,
        "email": user.email,
    })


# 8. Delete satu User
@require_POST
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    username = user.username
    user.delete()

    return JsonResponse({
        "message": f"User {username} berhasil dihapus"
    })


# 9. Delete semua Course
@require_POST
def delete_all_courses(request):
    total, details = Course.objects.all().delete()

    return JsonResponse({
        "message": "Proses penghapusan Course selesai",
        "deleted_count": total,
        "details": details,
    })


# 10. Delete semua User kecuali ID tertentu
@require_POST
def delete_users_except(request, pk):
    # Contoh: pertahankan user dengan ID pk
    users = User.objects.exclude(pk=pk)
    total, details = users.delete()

    return JsonResponse({
        "message": f"User selain ID {pk} telah diproses",
        "deleted_count": total,
        "details": details,
    })