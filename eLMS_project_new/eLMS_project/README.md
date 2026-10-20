eLMS - minimal Django app
=========================

Struktur ini dibuat berdasarkan permintaan untuk aplikasi e-LMS
yang berisi model Course, CourseMember, CourseContent, dan Comment
beserta views dan templates dasar.

Cara pakai (local):
1. buat virtualenv, install requirements.txt
   python -m venv venv
   source venv/bin/activate  # atau venv\Scripts\activate untuk Windows
   pip install -r requirements.txt
2. jalankan migrate & buat superuser:
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
3. jalankan server:
   python manage.py runserver

File penting:
- manage.py
- eLMS/settings.py
- coreapp/models.py, views.py, urls.py, admin.py
- coreapp/templates/ (basic templates)

Catatan:
- SECRET_KEY di settings.py harus diganti untuk produksi.
- DEBUG=True diatur untuk kemudahan development.
