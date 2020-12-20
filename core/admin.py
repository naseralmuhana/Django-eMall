from django.contrib import admin
from core import models as core_models


class StoreAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'store']
    list_filter = ['store']
    readonly_fields = ('slug',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    readonly_fields = ('slug',)


admin.site.register(core_models.Store, StoreAdmin)
admin.site.register(core_models.Category, CategoryAdmin)
admin.site.register(core_models.Product, ProductAdmin)
