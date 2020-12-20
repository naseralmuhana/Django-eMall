from django.urls import path
from django.conf.urls.static import static
from eMall import settings

from core import views as core_views

app_name = 'core'

urlpatterns = [
    path('', core_views.IndexPageView.as_view(), name='index'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
