from django.contrib import admin
from .models import Course, CourseContent, CourseMember, Comment

# Daftarin semua tabel biar muncul di panel admin
admin.site.register(Course)
admin.site.register(CourseContent)
admin.site.register(CourseMember)
admin.site.register(Comment)