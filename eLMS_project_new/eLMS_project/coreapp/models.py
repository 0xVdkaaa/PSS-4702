from django.db import models
from django.contrib.auth.models import User

class Dosen(models.Model):
    nidn = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    fakultas = models.CharField(max_length=100)
    prodi = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Data Dosen"

    def __str__(self):
        return f"{self.nidn} - {self.nama}"

class Mahasiswa(models.Model):
    nim = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    angkatan = models.CharField(max_length=4)
    fakultas = models.CharField(max_length=100)
    prodi = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Data Mahasiswa"

    def __str__(self):
        return f"{self.nim} - {self.nama}"

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    teacher = models.ForeignKey(Dosen, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Mata Kuliah"

    def __str__(self):
        return self.name

class CourseMember(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Peserta Mata Kuliah"

    def __str__(self):
        return f"{self.user.username} di {self.course.name}"

class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='contents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Materi Mata Kuliah"

    def __str__(self):
        return self.title

class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Komentar"

    def __str__(self):
        return f"Komentar {self.user.username}"