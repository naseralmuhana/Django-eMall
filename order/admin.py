from django.contrib import admin
from order import models as order_models

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'product_cart','price','quantity','amount',)
    list_filter = ('user_id',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name',
                    'phone', 'address', 'total', 'status')
    list_filter = ('status', 'create_at')
    # readonly_fields = ('first_name', 'last_name', 'email', 'phone', 'zip_code',
    #                    'address', 'city',  'total', 'user')



class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity',
                    'price', 'total', 'modified','deliver_time','color_Choiced','size_Choiced',)
    readonly_fields = ('product', 'quantity', 'price', 'total')



admin.site.register(order_models.ShopCart,ShopCartAdmin)
admin.site.register(order_models.OrderDetail, OrderDetailAdmin)
admin.site.register(order_models.Order, OrderAdmin)