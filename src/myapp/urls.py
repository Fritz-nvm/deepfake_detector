from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('detect/', views.DeepfakeDetectionView.as_view(), name='detect'),

 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)