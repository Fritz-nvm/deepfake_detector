from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_form/', views.upload_and_analyze, name='upload-form'),
    path('result/<int:file_id>/', views.analysis_result, name='analysis_result'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)