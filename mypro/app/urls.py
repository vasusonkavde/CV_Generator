from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accept/', views.accept),
    path('preview/<uid>', views.preview, name='preview'),
    path('resume1/<uid>', views.resume1),
    path('edit/<uid>', views.edit),
    path('Template/<uid>',views.template1),
    path('choose-template/<int:uid>', views.choose_template, name='choose_template'),
    path('download-pdf/<template_id>/<uid>', views.download_pdf, name='download_pdf'),
    path('home',views.home),
    path('templates',views.templates),
    path('register',views.register),
    path("login",views.user_login),
    path("logout",views.user_logout),
]

if settings.DEBUG: 
     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
