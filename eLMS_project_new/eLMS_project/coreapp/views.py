from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Max, Min, Avg, Count
from django.contrib.auth.models import User
from .models import Course, Mahasiswa, CourseMember, CourseContent, Comment

# View buat halaman utama (Dashboard)
def home(request):
    # Kalau nama file template lu beda (misal index.html), tinggal ganti aja ya
    return render(request, 'core.html')

# View buat data Mahasiswa
def mahasiswa_list(request):
    mahasiswa = Mahasiswa.objects.all()
    return render(request, 'mahasiswa_list.html', {'mahasiswa': mahasiswa})

# View buat daftar Course
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

# View buat API statistik Course JSON
def courseStat(request):
    courses = Course.objects.all()
    stats = courses.aggregate(
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price')
    )
    
    # Ambil course paling murah & mahal
    cheapest = Course.objects.filter(price=stats['min_price']) if stats['min_price'] is not None else []
    expensive = Course.objects.filter(price=stats['max_price']) if stats['max_price'] is not None else []
    
    # Ambil course paling populer & nggak populer (udah diganti jadi 'coursemember' biar nggak error)
    popular = Course.objects.annotate(member_count=Count('coursemember')).order_by('-member_count')[:1]
    unpopular = Course.objects.annotate(member_count=Count('coursemember')).order_by('member_count')[:1]
    
    result = {
        'course_count': len(courses),
        'courses': stats,
        'cheapest': serializers.serialize('python', cheapest) if cheapest else [],
        'expensive': serializers.serialize('python', expensive) if expensive else [],
        'popular': serializers.serialize('python', popular),
        'unpopular': serializers.serialize('python', unpopular)
    }
    return JsonResponse(result, safe=False)

# View buat API statistik User JSON
def userStat(request):
    users = User.objects.all()
    result = {
        'total_users': users.count()
    }
    return JsonResponse(result, safe=False)