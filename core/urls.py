from django.urls import path
from django.conf.urls.static import static
from eMall import settings

from core import views as core_views

app_name = 'core'

urlpatterns = [
    path('', core_views.IndexPageView.as_view(), name='index'),
    path('<slug>', core_views.store_type_list, name='store_type_list'),
    path('<type_slug>/<slug>', core_views.store_products_list, name='store_products_list'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
