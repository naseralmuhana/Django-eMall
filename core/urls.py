from django.urls import path
from django.conf.urls.static import static
from eMall import settings

from core import views as core_views

app_name = 'core'

urlpatterns = [
    path('', core_views.IndexPageView.as_view(), name='index'),
    path('<slug>-type/', core_views.store_type_list, name='store_type_list'),
    path('<type_slug>-type/<slug>/', core_views.store_products_list, name='store_products_list'),
    path('<c_store_type>-type/<store_slug>/<slug>/', core_views.category_products_list, name='category_products_list'),
    path('<p_store_type>-type/<store_slug>/<category_slug>/<slug>/', core_views.product_detail, name='product_detail'),
    path('<pr_store_type>-type/<store_slug>/<category_slug>/<slug>/reviews/', core_views.reviews_list, name='reviews_list'),
    path('favourite-product/<slug>/', core_views.favourite_product, name="favourite_product"),
    path('add-comment/<int:id>', core_views.add_comment, name="add_comment"),
    path('delete-comment/<int:proid>', core_views.delete_comment, name="delete_comment"),
    path('search', core_views.SearchView.as_view(), name='search_result'),
    path('Quick_view/', core_views.Quick_View, name='Quick_View'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
