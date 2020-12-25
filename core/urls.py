from django.urls import path
from django.conf.urls.static import static
from eMall import settings

from core import views as core_views

app_name = 'core'

urlpatterns = [
    path('', core_views.IndexPageView.as_view(), name='index'),
    path('result', core_views.SearchView.as_view(), name='search_result'),
    path('<slug>/', core_views.store_type_list, name='store_type_list'),
    path('<type_slug>/<slug>/', core_views.store_products_list, name='store_products_list'),
    path('<c_store_type>/<store_slug>/<slug>/', core_views.category_products_list, name='category_products_list'),
    path('<p_store_type>/<store_slug>/<category_slug>/<slug>/', core_views.product_detail, name='product_detail'),
    
    path('add-remove-favourite-product/<slug>', core_views.add_favourite_product, name="add_favourite_product"),
    path('add-comment/<int:id>', core_views.add_comment, name="add_comment"),
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
