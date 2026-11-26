from django.contrib import admin
from .models import Course, CourseMember, CourseContent, Comment, Enrollment

# Register your models here.
admin.site.register(CourseMember)
admin.site.register(Course)
admin.site.register(CourseContent)
admin.site.register(Comment)

admin.site.register(Enrollment)
