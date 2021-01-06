from django import forms
from core import models as core_models
from order import models as order_models


class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    class Meta:
        model = core_models.Product
        fields = "__all__"
        exclude = ["favourite", "slug"]

    def __init__(self, store_name ,*args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = core_models.Category.objects.filter(store__name=store_name)


class CategoryForm(forms.ModelForm):

    class Meta:
        model = core_models.Category
        fields = "__all__"
        exclude = ["slug"]

    def __init__(self, store_name ,*args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['store'].queryset = core_models.Store.objects.filter(name=store_name)


class BrandForm(forms.ModelForm):

    class Meta:
        model = core_models.Brand
        fields = "__all__"
        exclude = ["slug"]


class OrderForm(forms.ModelForm):

    class Meta:
        model = order_models.Order
        fields = ["status",]