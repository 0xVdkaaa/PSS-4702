from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Count
from .models import Course, CourseMember, CourseContent

def home(request):
    # --- 1. TAMPILAN GUEST (BELUM LOGIN) ---
    if not request.user.is_authenticated:
        # OPTIMASI ORM: Pake select_related('teacher')
        courses = Course.objects.select_related('teacher').all()
        context = {
            'courses': courses,
            'total_course': courses.count(),
            'total_user': User.objects.count(),
            'total_modul': CourseContent.objects.count(),
            'is_guest': True,
        }
        return render(request, 'core.html', context)

    # --- 2. KALAU ADMIN (SUPERUSER) TENDANG KE DATABASE ---
    if request.user.is_superuser:
        return redirect('/admin/')

    # --- 3. CEK ROLE USER (DOSEN / MAHASISWA) ---
    is_dosen = request.user.groups.filter(name='Dosen').exists()
    is_mahasiswa = request.user.groups.filter(name='Mahasiswa').exists()
    
    courses = []
    total_course = 0
    total_modul = 0
    total_siswa = 0

    if is_dosen:
        # DOSEN: Pake select_related('teacher')
        courses = Course.objects.select_related('teacher').filter(teacher__email=request.user.email)
        total_course = courses.count()
        total_modul = CourseContent.objects.filter(course__in=courses).count()
        total_siswa = CourseMember.objects.filter(course__in=courses).count()
        
    elif is_mahasiswa:
        # MAHASISWA: Pake select_related('course__teacher')
        enrollments = CourseMember.objects.select_related('course__teacher').filter(user=request.user)
        courses = [e.course for e in enrollments]
        total_course = len(courses)
        if courses:
            total_modul = CourseContent.objects.filter(course__in=courses).count()
        
    else:
        # DEFAULT (User Umum Terdaftar): Pake select_related('teacher')
        courses = Course.objects.select_related('teacher').all()
        total_course = courses.count()
        total_modul = CourseContent.objects.count()

    context = {
        'courses': courses,
        'total_course': total_course,
        'total_modul': total_modul,
        'total_siswa': total_siswa,
        'total_user': User.objects.count(),
        'is_dosen': is_dosen,
        'is_mahasiswa': is_mahasiswa,
        'is_guest': False,
    }
    return render(request, 'core.html', context)

# --- FUNGSI API BUAT GRAFIK CHART.JS ---
def course_stat_api(request):
    courses = Course.objects.annotate(total_siswa=Count('coursemember'))
    labels = []
    data = []
    
    for c in courses:
        labels.append(c.name)
        data.append(c.total_siswa)
        
    return JsonResponse({
        'labels': labels,
        'data': data
    })