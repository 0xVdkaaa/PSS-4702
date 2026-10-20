from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Count, Min, Max, Avg
from .models import Course, CourseMember
import csv
import os
from django.conf import settings

# --- FUNGSI TUGAS 3: IMPORT CSV ---
def testing(request):
    base_dir = settings.BASE_DIR
    
    # Import Data User
    user_path = os.path.join(base_dir, 'user-data.csv')
    if os.path.exists(user_path):
        with open(user_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not User.objects.filter(email=row['email']).exists():
                    User.objects.create_user(
                        username=row['username'],
                        email=row['email'],
                        password=row['password']
                    )
    
    # Import Data Course
    course_path = os.path.join(base_dir, 'course-data.csv')
    if os.path.exists(course_path):
        with open(course_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                teacher = User.objects.filter(email=row['teacher_email']).first()
                if teacher and not Course.objects.filter(name=row['name']).exists():
                    Course.objects.create(
                        name=row['name'],
                        description=row['description'],
                        price=row['price'],
                        image=row['image'],
                        teacher=teacher
                    )

    # Import Data Member
    member_path = os.path.join(base_dir, 'member-data.csv')
    if os.path.exists(member_path):
        with open(member_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                course = Course.objects.filter(name=row['course_name']).first()
                user = User.objects.filter(email=row['user_email']).first()
                
                if course and user and not CourseMember.objects.filter(course=course, user=user).exists():
                    CourseMember.objects.create(
                        course=course,
                        user=user,
                        roles=row['roles']
                    )

    return HttpResponse("Proses Import Data Selesai! Semua data dari CSV udah masuk ke database.")

# --- FUNGSI TUGAS 4: RELASI DAN AGREGASI ---
def course_list(request):
    # Relasi dan Agregasi (Count)
    courses = Course.objects.select_related('teacher').annotate(total_member=Count('members'))
    
    html = "<h1>Daftar Mata Kuliah (Relasi & Agregasi)</h1>"
    html += "<table border='1' cellpadding='10' style='border-collapse: collapse;'>"
    html += "<tr><th>Nama Kursus</th><th>Pengajar (Relasi)</th><th>Harga</th><th>Jumlah Siswa (Agregasi)</th></tr>"
    
    for c in courses:
        html += f"<tr><td>{c.name}</td><td>{c.teacher.username}</td><td>Rp {c.price}</td><td>{c.total_member} Siswa</td></tr>"
    
    html += "</table>"
    
    # Agregasi Global (Min, Max, Avg)
    stats = Course.objects.aggregate(
        termurah=Min('price'),
        termahal=Max('price'),
        rata_rata=Avg('price')
    )
    
    html += "<h2>Statistik Harga Kursus</h2><ul>"
    html += f"<li>Harga Termurah: Rp {stats['termurah']}</li>"
    html += f"<li>Harga Termahal: Rp {stats['termahal']}</li>"
    rata = int(stats['rata_rata']) if stats['rata_rata'] else 0
    html += f"<li>Rata-rata Harga: Rp {rata}</li></ul>"

    return HttpResponse(html)