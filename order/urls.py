from django.urls import path
from django.conf.urls.static import static
from eMall import settings

from order import views as order_views

app_name = 'order'

urlpatterns = [
    
    path('deletefromcart/<int:id>/',order_views.deletefromcart,name = 'deletefromcart'),
    path('addtoshpcart/<int:id>/',order_views.addtoshpcart,name = 'addtoshpcart'),
    path('shopcart/',order_views.shopcart,name = 'shopcart'),
    path('updatefromcart/<int:id>/',order_views.updatefromcart,name = 'updatefromcart'),
    path('checkout/',order_views.checkout,name = 'checkout'),
    path('checkoutcomplete/<int:id>/',order_views.checkout_complete,name = 'checkoutcomplete'),
    path('checkoutdelete/<int:id>/',order_views.checkout_delete,name = 'checkoutdelete'),
    
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
