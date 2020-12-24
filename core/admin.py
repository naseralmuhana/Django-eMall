from django.contrib import admin
from core import models as core_models


class StoreAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'store',)
    list_filter = ('store',)
    readonly_fields = ('slug',)


class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'category', 'store_name',)
    list_filter = ('category','category__store__name',)
    readonly_fields = ('slug',)
    


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'create_at']
    list_filter = ['rating', 'product__category__store', 'product__category', 'user', 'product']
    readonly_fields = ('product','user', 'rating', 'review', 'create_at')


admin.site.register(core_models.StoreType)
admin.site.register(core_models.Store, StoreAdmin)
admin.site.register(core_models.Category, CategoryAdmin)
admin.site.register(core_models.Brand)
admin.site.register(core_models.Product, ProductAdmin)
admin.site.register(core_models.Comment, CommentAdmin)


