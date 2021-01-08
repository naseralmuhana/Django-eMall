from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from account import forms as account_forms
from account import models as account_models
from core import models as core_models
from core import views as core_views
from order.models import Order, OrderDetail


def register_view(request):

    if request.method == 'POST':
        form = account_forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            user = authenticate(username=username, password=password1)
            login(request, user)
            messages.success(
                request, f"Welcome Mr.{username}.")
            return redirect('core:index')
    else:
        form = account_forms.UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
        else:
            messages.warning(
                request, "Something went wrong, check your information. Or Register if you don't have an account.")
            return redirect('core:index')
        if 'next' in request.POST:
            messages.success(
                request, f"Welcome back, Mr.{username}.")
            return HttpResponseRedirect(request.POST.get('next'))
        else:
            messages.success(
                request, f"Welcome back, Mr.{username}.")
            return redirect('core:index')


@login_required(login_url='/accounts/login/')
def profile(request):
    if request.method == 'POST':
        form = account_forms.ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
    else:
        form = account_forms.ProfileUpdateForm(instance=request.user)

    profile = account_models.UserRegistration.objects.filter(
        username=request.user.username)[0]
    wishlist_count = core_models.Product.objects.filter(
        favourite=request.user.id).count()
    orders_count = Order.objects.filter(
        user_id=request.user.id).order_by('-create_at').count()
    context = {
        'profile_exist': True,
        'profile': profile,
        'wishlist_count': wishlist_count,
        'form': form,
        'orders_count': orders_count,
    }
    context.update(core_views.needed_everywhere(request.user))
    return render(request, 'account/profile.html', context)


@login_required(login_url='/accounts/login/')
def wishlist_view(request):
    profile = account_models.UserRegistration.objects.filter(
        username=request.user.username)[0]
    wishlist_list = core_models.Product.objects.filter(
        favourite=request.user.id).order_by('name')
    wishlist_count = wishlist_list.count()
    orders_count = Order.objects.filter(
        user_id=request.user.id).order_by('-create_at').count()
    context = {
        'wishlist_exist': True,
        'profile': profile,
        'wishlist_list': wishlist_list,
        'wishlist_count': wishlist_count,
        'orders_count': orders_count,
    }
    context.update(core_views.needed_everywhere(request.user))
    return render(request, 'account/profile.html', context)


@login_required(login_url='/accounts/login/')
def orders_view(request):
    profile = account_models.UserRegistration.objects.filter(
        username=request.user.username)[0]
    orders_list = Order.objects.filter(
        user_id=request.user.id).order_by('-create_at')
    orders_count = orders_list.count()
    wishlist_count = core_models.Product.objects.filter(
        favourite=request.user.id).count()
    context = {
        'orders_exist': True,
        'profile': profile,
        'orders_list': orders_list,
        'wishlist_count': wishlist_count,
        'orders_count': orders_count,
    }
    context.update(core_views.needed_everywhere(request.user))
    return render(request, 'account/profile.html', context)


@login_required(login_url='/accounts/login/')
def order_details(request, id):
    profile = account_models.UserRegistration.objects.filter(
        username=request.user.username)[0]
    orders_list = Order.objects.filter(
        user_id=request.user.id).order_by('-create_at')
    orders_count = orders_list.count()
    wishlist_count = core_models.Product.objects.filter(
        favourite=request.user.id).count()
    order_details = OrderDetail.objects.filter(order_id=id)
    context = {
        'order_details': True,
        'profile': profile,
        'order_details_exist': 'exist',
        'order_details': order_details,
        'wishlist_count': wishlist_count,
        'orders_count': orders_count,
    }
    context.update(core_views.needed_everywhere(request.user))
    return render(request, 'account/profile.html', context)
