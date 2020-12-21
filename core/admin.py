from django.contrib import admin
from core import models as core_models

# class ProductImageAdmin(admin.StackedInline):
#     model = core_models.ProductImage
 

class StoreAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'store',)
    list_filter = ('store',)
    readonly_fields = ('slug',)


class ProductAdmin(admin.ModelAdmin):
    # inlines = [ProductImageAdmin]
    list_display = ('name', 'category', 'store_name',)
    list_filter = ('category','category__store__name',)
    readonly_fields = ('slug',)
    
    # class Meta:
    #    model = core_models.Product


admin.site.register(core_models.StoreType)
admin.site.register(core_models.Store, StoreAdmin)
admin.site.register(core_models.Category, CategoryAdmin)
admin.site.register(core_models.Product, ProductAdmin)


