from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required

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
    name = check_on_slug(store_slug)
    if name is None:
        return HttpResponse('<h1>Post Not Found</h1>')

    store_products = core_models.Product.objects.filter(
        category__store__name=name).order_by('-create_at')
    store_name = store_products[0].category.store.name
    store_slug = store_products[0].category.store.slug
    store_type_name = store_products[0].category.store.storetype.name
    store_type_slug = store_products[0].category.store.storetype.slug
    store_logo = store_products[0].category.store.logo

    context = {
        'store_products': store_products,
        'store_name': store_name,
        'store_slug': store_slug,
        'store_type_name': store_type_name,
        'store_type_slug': store_type_slug,
        'store_logo': store_logo,
        'store_categories': store_categories(name),
        'products_paginator': paginate_view(request, store_products)
    }
    context.update(needed_everywhere())
    return render(request, 'core/products_list.html', context)


def category_products_list(request, c_store_type, store_slug, slug):

    category_slug = core_models.Category.objects.filter(slug__iexact=slug)
    name = check_on_slug(category_slug)
    if name is None:
        return HttpResponse('<h1>Post Not Found</h1>')

    category_products = core_models.Product.objects.filter(
        category__name=name).order_by('-create_at')
    category_name = category_products[0].category.name
    store_name = category_products[0].category.store.name
    store_type_name = category_products[0].category.store.storetype.name

    context = {
        'category_products': category_products,
        'category_name': category_name,
        'store_name': store_name,
        'store_slug': store_slug,
        'store_type_name': store_type_name,
        'store_type_slug': c_store_type,
        'store_categories': store_categories(store_name),
        'products_paginator': paginate_view(request, category_products)
    }
    context.update(needed_everywhere())
    return render(request, 'core/products_list.html', context)


def product_detail(request, p_store_type, store_slug, category_slug, slug):
    product_slug = core_models.Product.objects.filter(slug__iexact=slug)
    name = check_on_slug(product_slug)
    if name is None:
        return HttpResponse('<h1>Post Not Found</h1>')

    product = name
    category_name = product.category.name
    store_name = product.category.store.name
    store_type_name = product.category.store.storetype.name
    similar_products = core_models.Product.objects.filter(
        ~Q(name=product), category__name=category_name)

    context = {
        'product': product,
        'category_name': category_name,
        'store_name': store_name,
        'store_slug': store_slug,
        'store_type_name': store_type_name,
        'store_type_slug': p_store_type,
        'store_categories': store_categories(store_name),
        'similar_products': similar_products,
    }
    context.update(needed_everywhere())
    return render(request, 'core/product_details.html', context)


def add_favourite_product(request, slug):

    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(core_models.Product, slug=slug)
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
    else:
        product.favourite.add(request.user)
    return HttpResponseRedirect(url)


def add_comment(request, id):

    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = core_models.CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user
            data = core_models.Comment()
            data.product_id = id
            data.user_id = current_user.id
            data.review = form.cleaned_data['review']
            data.rating = form.cleaned_data['rating']
            data.save()
        else:
            return redirect(url)
    return HttpResponseRedirect(url)


# extra
# function to check if the slug is exist and return none if not.
def check_on_slug(slug):

    if slug.exists():
        slug = slug.first()
        return slug
    else:
        return None


def store_categories(name):
    store_categories_dict = {}
    store_categories = core_models.Category.objects.filter(
        store__name=name).order_by('name')
    for category in store_categories:
        store_categories_dict[category] = core_models.Product.objects.filter(
            category__name=category).count()
    return store_categories_dict


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
    paginator = Paginator(products, 8)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    return products_paginator
