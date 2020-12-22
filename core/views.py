from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core import models as core_models


class IndexPageView(TemplateView):

    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context.update(needed_everywhere())
        return context


def store_type_list(request, slug):

    type_slug = core_models.StoreType.objects.filter(slug__iexact=slug)
    slug = check_on_slug(type_slug)
    if slug is None:
        return HttpResponse('<h1>Post Not Found</h1>')
    type_stores_list = core_models.Store.objects.filter(
        storetype=slug).order_by('-create_at')

    context = {
        'type_stores_list': type_stores_list,
    }
    context.update(needed_everywhere())
    return render(request, 'core/index.html', context)


def store_products_list(request, type_slug, slug):

    store_slug = core_models.Store.objects.filter(slug__iexact=slug)
    slug = check_on_slug(store_slug)
    if slug is None:
        return HttpResponse('<h1>Post Not Found</h1>')
    store_products = core_models.Product.objects.filter(
        category__store=slug).order_by('-create_at')
    context = {
        'store_products': store_products,
        'store_name': store_products[0].category.store.name,
        'store_type_name': store_products[0].category.store.storetype.name,
        'store_type_slug': store_products[0].category.store.storetype.slug,
        'products_paginator': paginate_view(request, store_products)
    }
    context.update(needed_everywhere())
    return render(request, 'core/products_list.html', context)


# extra

# function to check if the slug is exist and return none if not.
def check_on_slug(slug):

    if slug.exists():
        slug = slug.first()
        return slug
    else:
        return None


def needed_everywhere():
    context = {}
    all_products = {}
    all_stores = core_models.Store.objects.all().order_by('-create_at')

    for store in all_stores:
        all_products[store.name] = core_models.Product.objects.filter(
            category__store__name=store.name).order_by('-create_at')[:12]

    context['all_stores'] = all_stores
    context['all_products'] = all_products
    context['store_types'] = core_models.StoreType.objects.all()

    return context


def paginate_view(request, products):

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 4)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    return products_paginator
