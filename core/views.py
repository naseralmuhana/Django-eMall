from django.shortcuts import render
from django.views.generic import TemplateView

from core import models as core_models


class IndexPageView(TemplateView):

    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['products'] = core_models.Product.objects.all
        context['photos'] = core_models.ProductImage.objects.filter(product__name='red shirt')
        return context
