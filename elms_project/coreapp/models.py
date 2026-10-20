from django.db import models
from django.contrib.auth.models import User

# 1. Tabel Course (Mata Kuliah)
class Course(models.Model):
    name = models.CharField('Nama Kursus', max_length=200)
    description = models.TextField('Deskripsi')
    price = models.IntegerField('Biaya Kursus', default=0)
    image = models.CharField('URL Gambar', max_length=200, null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# 2. Tabel Course Content (Materi Kursus)
class CourseContent(models.Model):
    name = models.CharField('Judul Materi', max_length=200)
    description = models.TextField('Deskripsi Materi')
    video_url = models.CharField('URL Video', max_length=200, null=True, blank=True)
    file_attachment = models.CharField('URL File', max_length=200, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.name} - {self.name}"

# 3. Tabel Course Member (Siswa yang gabung ke kursus)
class CourseMember(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolled_courses')
    roles = models.CharField('Peran', max_length=50, default='std') # std = student
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"

# 4. Tabel Comment (Komentar di materi)
class Comment(models.Model):
    content = models.ForeignKey(CourseContent, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField('Komentar')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Komentar {self.user.username} di {self.content.name}"