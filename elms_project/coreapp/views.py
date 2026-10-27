from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.db.models import Count, Max, Min, Avg
from django.contrib.auth.models import User
from .models import Course, CourseMember, CourseContent, Comment

def courseStat(request):
    courses = Course.objects.all()
    stats = courses.aggregate(
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price')
    )
    cheapest = Course.objects.filter(price=stats['min_price'])
    expensive = Course.objects.filter(price=stats['max_price'])
    
    popular = Course.objects.annotate(member_count=Count('members')).order_by('-member_count')[:5]
    unpopular = Course.objects.annotate(member_count=Count('members')).order_by('member_count')[:5]

    result = {
        'course_count': len(courses),
        'courses': stats,
        'cheapest': serializers.serialize('python', cheapest),
        'expensive': serializers.serialize('python', expensive),
        'popular': serializers.serialize('python', popular),
        'unpopular': serializers.serialize('python', unpopular)
    }
    return JsonResponse(result, safe=False)

def userStat(request):
    non_admins = User.objects.filter(is_superuser=False)
    
    users_with_courses = non_admins.annotate(course_count=Count('enrolled_courses')).filter(course_count__gt=0)
    users_without_courses = non_admins.annotate(course_count=Count('enrolled_courses')).filter(course_count=0)
    
    avg_courses = non_admins.annotate(course_count=Count('enrolled_courses')).aggregate(Avg('course_count'))
    
    top_user = users_with_courses.order_by('-course_count')[:1]
    top_user_data = [{'username': u.username, 'email': u.email, 'total_courses': u.course_count} for u in top_user]
    
    no_course_data = [{'username': u.username, 'email': u.email} for u in users_without_courses]

    result = {
        'total_non_admin_users': non_admins.count(),
        'total_users_with_courses': users_with_courses.count(),
        'total_users_without_courses': users_without_courses.count(),
        'average_courses_per_user': avg_courses['course_count__avg'] or 0,
        'top_user': top_user_data,
        'users_no_courses': no_course_data
    }
    return JsonResponse(result, safe=False)

def course_list(request):
    return HttpResponse("Ini halaman daftar courses (masih dummy biar nggak error).")

def home(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard e-LMS</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin-top: 10%; background-color: #f4f7f6; color: #333; }
            h1 { color: #2c3e50; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            .btn { display: block; width: 80%; padding: 15px; margin: 15px auto; text-decoration: none; color: white; background-color: #3498db; border-radius: 8px; font-size: 18px; font-weight: bold; transition: 0.3s; }
            .btn:hover { background-color: #2980b9; }
            .btn-admin { background-color: #27ae60; }
            .btn-admin:hover { background-color: #2ecc71; }
            .btn-silk { background-color: #9b59b6; }
            .btn-silk:hover { background-color: #8e44ad; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Selamat Datang di e-LMS</h1>
            <p>Pilih menu laporan tugas Pertemuan 7 di bawah ini:</p>
            <a href="/admin/" target="_blank" class="btn btn-admin">⚙️ Halaman Django Admin</a>
            <a href="/silk/" target="_blank" class="btn btn-silk">📊 Buka Dashboard Silk</a>
            <a href="/course-stat/" target="_blank" class="btn">📚 Statistik Course (JSON)</a>
            <a href="/user-stat/" target="_blank" class="btn">👥 Statistik User (JSON)</a>
            
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)