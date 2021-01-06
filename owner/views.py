from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from core import models as core_models
from order import models as order_models
from account import models as account_models

from core import views as core_views
from owner import forms as owner_forms


@login_required(login_url='/accounts/login/')
def product_list(request):

    owner_check = account_models.OwnerProfile.objects.filter(user=request.user)[
        0]
    if owner_check:
        store_name = owner_check.store.name
        store_join_date = owner_check.store.create_at
        store_image = owner_check.store.image
        context = {
            'products': products,
            'product_list': 'exist',
            'product_count': product_count(store_name),
            'overall_sales': overall_sales(store_name),
            'store_name': store_name,
            'store_join_date': store_join_date,
            'store_image': store_image,
        }
        context.update(core_views.needed_everywhere(request.user))
        return render(request, 'owner/product.html', context)
    else:
        return HttpResponse('<h1>Post Not Found</h1>')


@login_required(login_url='/accounts/login/')
def add_product(request):
    owner_check = account_models.OwnerProfile.objects.filter(user=request.user)[
        0]
    if owner_check:
        store_name = owner_check.store.name
        store_join_date = owner_check.store.create_at
        store_image = owner_check.store.image
        url = request.META.get('HTTP_REFERER')
        if request.method == "POST":
            form = owner_forms.ProductForm(
                store_name, request.POST, request.FILES)
            if form.is_valid():
                print('shit')
                form.save()
            return HttpResponseRedirect(url)
        else:
            form = owner_forms.ProductForm(store_name)
            context = {
                'form': form,
                'add_product': 'true',
                'product_count': product_count(store_name),
                'overall_sales': overall_sales(store_name),
                'store_name': store_name,
                'store_join_date': store_join_date,
                'store_image': store_image,
            }
            context.update(core_views.needed_everywhere(request.user))
            return render(request, 'owner/product.html', context)

    else:
        return HttpResponse('<h1>Post Not Found</h1>')


@login_required(login_url='/accounts/login/')
def update_product(request, slug):
    owner_check = account_models.OwnerProfile.objects.filter(user=request.user)[
        0]

    if owner_check:
        store_name = owner_check.store.name
        store_join_date = owner_check.store.create_at
        store_image = owner_check.store.image
        url = request.META.get('HTTP_REFERER')
        product = core_models.Product.objects.get(slug=slug)
        if request.method == "POST":
            form = owner_forms.ProductForm(
                store_name, request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(url)
        else:
            form = owner_forms.ProductForm(store_name, instance=product)
            context = {
                'form': form,
                'update_product': 'true',
                'product_count': product_count(store_name),
                'overall_sales': overall_sales(store_name),
                'store_name': store_name,
                'store_join_date': store_join_date,
                'store_image': store_image,
            }
            context.update(core_views.needed_everywhere(request.user))
            return render(request, 'owner/product.html', context)
    else:
        return HttpResponse('<h1>Post Not Found</h1>')


@ login_required(login_url='/accounts/login/')
def delete_product(request, slug):
    owner_check = account_models.OwnerProfile.objects.filter(user=request.user)[
        0]
    if owner_check:
        url = request.META.get('HTTP_REFERER')
        product_name = core_models.Product.objects.filter(
            slug=slug)[0]
        core_models.Product.objects.filter(slug=slug).delete()
        return HttpResponseRedirect(url)
    else:
        return HttpResponse('<h1>Post Not Found</h1>')


@ login_required(login_url='/accounts/login/')
def add_category(request):
    owner_check = account_models.OwnerProfile.objects.filter(user=request.user)[
        0]
    if owner_check:
        store_name = owner_check.store.name
        store_join_date = owner_check.store.create_at
        store_image = owner_check.store.image
        url = request.META.get('HTTP_REFERER')
        if request.method == "POST":
            form = owner_forms.CategoryForm(store_name, request.POST, request.FILES)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(url)
        else:
            form = owner_forms.CategoryForm(store_name)
            context = {
                'form': form,
                'add_category': 'ture',
                'product_count': product_count(store_name),
                'overall_sales': overall_sales(store_name),
                'store_name': store_name,
                'store_join_date': store_join_date,
                'store_image': store_image,
            }
            context.update(core_views.needed_everywhere(request.user))
            return render(request, 'owner/product.html', context)

    else:
        return HttpResponse('<h1>Post Not Found</h1>')


@ login_required(login_url='/accounts/login/')
def add_brand(request):
    owner_check = account_models.OwnerProfile.objects.filter(user=request.user)[
        0]
    if owner_check:
        store_name = owner_check.store.name
        store_join_date = owner_check.store.create_at
        store_image = owner_check.store.image
        url = request.META.get('HTTP_REFERER')
        if request.method == "POST":
            form = owner_forms.BrandForm(request.POST)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(url)
        else:
            form = owner_forms.BrandForm()
            context = {
                'form': form,
                'add_brand': 'ture',
                'product_count': product_count(store_name),
                'overall_sales': overall_sales(store_name),
                'store_name': store_name,
                'store_join_date': store_join_date,
                'store_image': store_image,
            }
            context.update(core_views.needed_everywhere(request.user))
            return render(request, 'owner/product.html', context)

    else:
        return HttpResponse('<h1>Post Not Found</h1>')



def overall_sales(store_name):
    sum = 0
    orders = order_models.OrderDetail.objects.filter(
        product__category__store__name=store_name)
    for order in orders:
        sum += order.total
    return sum


def product_count(store_name):
    products = core_models.Product.objects.filter(
        category__store__name=store_name).order_by('-create_at')
    product_count = products.count()
    return product_count
