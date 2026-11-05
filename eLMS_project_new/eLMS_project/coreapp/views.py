from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Count
from django.contrib import messages
from .models import Course, CourseMember, CourseContent

def home(request):
    if not request.user.is_authenticated:
        courses = Course.objects.select_related('teacher').all()
        context = {
            'courses': courses,
            'total_course': courses.count(),
            'total_user': User.objects.count(),
            'total_modul': CourseContent.objects.count(),
            'is_guest': True,
        }
        return render(request, 'core.html', context)

    if request.user.is_superuser:
        return redirect('/admin/')

    is_dosen = request.user.groups.filter(name='Dosen').exists()
    is_mahasiswa = request.user.groups.filter(name='Mahasiswa').exists()
    
    courses = []
    other_courses = [] 
    total_course = 0
    total_modul = 0
    total_siswa = 0

    if is_dosen:
        courses = Course.objects.select_related('teacher').filter(teacher__email=request.user.email)
        total_course = courses.count()
        total_modul = CourseContent.objects.filter(course__in=courses).count()
        total_siswa = CourseMember.objects.filter(course__in=courses).count()
        
    elif is_mahasiswa:
        enrollments = CourseMember.objects.select_related('course__teacher').filter(user=request.user)
        courses = [e.course for e in enrollments]
        total_course = len(courses)
        if courses:
            total_modul = CourseContent.objects.filter(course__in=courses).count()
            
        enrolled_ids = [c.id for c in courses]
        other_courses = Course.objects.select_related('teacher').exclude(id__in=enrolled_ids)
        
    else:
        courses = Course.objects.select_related('teacher').all()
        total_course = courses.count()
        total_modul = CourseContent.objects.count()

    context = {
        'courses': courses,
        'other_courses': other_courses,
        'total_course': total_course,
        'total_modul': total_modul,
        'total_siswa': total_siswa,
        'total_user': User.objects.count(),
        'is_dosen': is_dosen,
        'is_mahasiswa': is_mahasiswa,
        'is_guest': False,
    }
    return render(request, 'core.html', context)

def course_stat_api(request):
    courses = Course.objects.annotate(total_siswa=Count('coursemember'))
    labels = []
    data = []
    for c in courses:
        labels.append(c.name)
        data.append(c.total_siswa)
    return JsonResponse({'labels': labels, 'data': data})

def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    moduls = CourseContent.objects.filter(course=course)
    
    is_enrolled = False
    is_teacher = False
    is_mahasiswa = False
    
    if request.user.is_authenticated:
        is_mahasiswa = request.user.groups.filter(name='Mahasiswa').exists()
        if course.teacher and course.teacher.email == request.user.email:
            is_teacher = True
        elif CourseMember.objects.filter(course=course, user=request.user).exists():
            is_enrolled = True

    context = {
        'course': course,
        'moduls': moduls,
        'is_enrolled': is_enrolled,
        'is_teacher': is_teacher,
        'is_mahasiswa': is_mahasiswa,
    }
    return render(request, 'course_detail.html', context)

def enroll_course(request, id):
    if request.method == 'POST' and request.user.is_authenticated:
        course = get_object_or_404(Course, id=id)
        if not CourseMember.objects.filter(course=course, user=request.user).exists():
            CourseMember.objects.create(course=course, user=request.user)
            messages.success(request, f"Berhasil bergabung dengan kelas {course.name}!")
        return redirect('course_detail', id=id)
    return redirect('login')

# --- FUNGSI UPLOAD MATERI (DISESUAIKAN DENGAN models.py) ---
def add_materi(request, id):
    course = get_object_or_404(Course, id=id)
    
    if not request.user.is_authenticated or not (course.teacher and course.teacher.email == request.user.email):
        messages.error(request, "Anda tidak memiliki akses untuk menambah materi di kelas ini.")
        return redirect('course_detail', id=id)

    if request.method == 'POST':
        judul_materi = request.POST.get('name')
        file_materi = request.FILES.get('file')

        if judul_materi:
            # Memakai 'title' sesuai dengan model CourseContent di models.py
            CourseContent.objects.create(
                course=course,
                title=judul_materi,
                file=file_materi
            )
            messages.success(request, "Materi berhasil ditambahkan ke dalam kelas!")
            return redirect('course_detail', id=id)
        else:
            messages.error(request, "Judul materi wajib diisi!")

    return render(request, 'course_content_list.html', {'course': course})