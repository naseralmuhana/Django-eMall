from django.urls import path
from django.conf.urls.static import static
from eMall import settings
from owner import views as owner_views


app_name = 'owner'

urlpatterns = [
    path('add-product/', owner_views.add_product, name="add_product"),
    path('add-category/', owner_views.add_category, name="add_category"),
    path('add-brand/', owner_views.add_brand, name="add_brand"),

    path('update-product/<slug>', owner_views.update_product, name="update_product"),
    path('delete-product/<slug>', owner_views.delete_product, name="delete_product"),
    path('products/', owner_views.product_list, name="product_list"),
    path('orders/', owner_views.orders_list, name="orders_list"),
    path('orders/<int:id>/', owner_views.order_details, name="order_details"),
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
