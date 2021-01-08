from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages

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
        products = core_models.Product.objects.filter(
            category__store__name=store_name).order_by('-create_at')
        context = {
            'products': products,
            'product_list': 'exist',
            'overall_sales': overall_sales(store_name),
            'store_name': store_name,
            'store_join_date': store_join_date,
            'store_image': store_image,
        }
        context.update(core_views.needed_everywhere(request.user))
        context.update(product_count(store_name))
        return render(request, 'owner/product.html', context)
    else:
        return HttpResponse('<h1>Post Not Found</h1>')


@login_required(login_url='/accounts/login/')
def orders_list(request):

    owner_check = account_models.OwnerProfile.objects.filter(user=request.user)[
        0]
    if owner_check:
        store_name = owner_check.store.name
        store_join_date = owner_check.store.create_at
        store_image = owner_check.store.image

        orders_id = order_models.OrderDetail.objects.filter(
            product__category__store__name=store_name).values('order_id').order_by('order_id').distinct()
        orders = []
        for id in orders_id:
            order = order_models.Order.objects.get(id=id['order_id'])
            orders.append(order)

        context = {
            'orders': orders,
            'orders_count': orders_id.count(),
            'orders_list': 'exist',
            'overall_sales': overall_sales(store_name),
            'store_name': store_name,
            'store_join_date': store_join_date,
            'store_image': store_image,
        }
        context.update(core_views.needed_everywhere(request.user))
        context.update(product_count(store_name))
        return render(request, 'owner/product.html', context)
    else:
        return HttpResponse('<h1>Post Not Found</h1>')


@login_required(login_url='/accounts/login/')
def order_details(request, id):
    owner_check = account_models.OwnerProfile.objects.filter(user=request.user)[
        0]
    if owner_check:
        store_name = owner_check.store.name
        store_join_date = owner_check.store.create_at
        store_image = owner_check.store.image

        order = order_models.Order.objects.get(id=id)
        if request.method == "POST":
            form = owner_forms.OrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
            return redirect('owner:orders_list')
        else:
            form = owner_forms.OrderForm(instance=order)

        orders_id = order_models.OrderDetail.objects.filter(
            product__category__store__name=store_name).values('order_id').order_by('order_id').distinct()
        orders = []
        for ido in orders_id:
            order = order_models.Order.objects.get(id=ido['order_id'])
            orders.append(order)

        order_details = order_models.OrderDetail.objects.filter(
            product__category__store__name=store_name, order_id=id).order_by('product_id')

        def total_price():
            total = 0
            for order in order_details:
                total += order.total
            return round(total, 2)

        context = {
            'form': form,
            'order_details': order_details,
            'orders_count': orders_id.count(),
            'orders_details': 'exist',
            'overall_sales': overall_sales(store_name),
            'store_name': store_name,
            'store_join_date': store_join_date,
            'store_image': store_image,
            'total_price': total_price(),
        }
        context.update(core_views.needed_everywhere(request.user))
        context.update(product_count(store_name))
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
                form.save()
            messages.success(
                request, f"Product has been Added.")
            return HttpResponseRedirect(url)
        else:
            form = owner_forms.ProductForm(store_name)
            context = {
                'form': form,
                'add_product': 'true',
                'overall_sales': overall_sales(store_name),
                'store_name': store_name,
                'store_join_date': store_join_date,
                'store_image': store_image,
            }
            context.update(core_views.needed_everywhere(request.user))
            context.update(product_count(store_name))
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
            messages.success(
                request, f"'{product.name}' has been Updated.")
            return HttpResponseRedirect(url)
        else:
            form = owner_forms.ProductForm(store_name, instance=product)
            context = {
                'form': form,
                'update_product': 'true',
                'overall_sales': overall_sales(store_name),
                'store_name': store_name,
                'store_join_date': store_join_date,
                'store_image': store_image,
            }
            context.update(core_views.needed_everywhere(request.user))
            context.update(product_count(store_name))
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
        messages.warning(
                request, f"'{product_name.name}' has been Deleted.")
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
            form = owner_forms.CategoryForm(
                store_name, request.POST, request.FILES)
            if form.is_valid():
                form.save()
            messages.success(
                request, f"Category has been Added.")
            return HttpResponseRedirect(url)
        else:
            form = owner_forms.CategoryForm(store_name)
            context = {
                'form': form,
                'add_category': 'ture',
                'overall_sales': overall_sales(store_name),
                'store_name': store_name,
                'store_join_date': store_join_date,
                'store_image': store_image,
            }
            context.update(core_views.needed_everywhere(request.user))
            context.update(product_count(store_name))
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
            messages.success(
                request, f"Brand has been Added.")
            return HttpResponseRedirect(url)
        else:
            form = owner_forms.BrandForm()
            context = {
                'form': form,
                'add_brand': 'ture',
                'overall_sales': overall_sales(store_name),
                'store_name': store_name,
                'store_join_date': store_join_date,
                'store_image': store_image,
            }
            context.update(core_views.needed_everywhere(request.user))
            context.update(product_count(store_name))
            return render(request, 'owner/product.html', context)

    else:
        return HttpResponse('<h1>Post Not Found</h1>')


def overall_sales(store_name):
    sum = 0
    orders = order_models.OrderDetail.objects.filter(
        product__category__store__name=store_name)
    for order in orders:
        sum += order.total
    return round(sum, 2)


def product_count(store_name):
    products = core_models.Product.objects.filter(
        category__store__name=store_name).order_by('-create_at')
    product_count = products.count()

    context = {
        'product_count': product_count,
    }
    return context
