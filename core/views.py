from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, resolve
from django.http import JsonResponse
import json
from core import models as core_models
from order import models as order_models
from account import models as account_models


class IndexPageView(TemplateView):

    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            check_user = self.request.user
        else:
            check_user = ''
        context['home_page'] = 'true'
        context.update(needed_everywhere(check_user))
        return context


def store_type_list(request, slug):

    type_slug = core_models.StoreType.objects.filter(slug__iexact=slug)
    slug = check_on_slug(type_slug)
    if slug is None:
        return HttpResponse('<h1>Post Not Found..</h1>')
    type_stores_list = core_models.Store.objects.filter(
        storetype=slug).order_by('-create_at')

    context = {
        'type_stores_list': type_stores_list,
    }
    if request.user.is_authenticated:
        check_user = request.user
    else:
        check_user = ''
    context.update(needed_everywhere(check_user))
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

    def overall_rating():
        if product_comments:
            sum, count = 0, 0
            for comment in product_comments:
                sum += comment.rating
                count += 1
        else:
            return 0
        return(round(sum/count, 1))

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
    if request.user.is_authenticated:
        check_user = request.user
    else:
        check_user = ''
    context.update(needed_everywhere(check_user))
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
    if request.user.is_authenticated:
        check_user = request.user
    else:
        check_user = ''
    context.update(needed_everywhere(check_user))
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

    product_comments = core_models.Comment.objects.filter(
        product__name=product).order_by('-create_at')
    product_comments_count = product_comments.count()

    def overall_rating():
        if product_comments:
            sum, count = 0, 0
            for comment in product_comments:
                sum += comment.rating
                count += 1
        else:
            return 0
        return(round(sum/count, 1))

    def rating_system():
        rate_system = {}
        count = 0
        rate_system['star1'] = product_comments.filter(rating=1).count()
        rate_system['star2'] = product_comments.filter(rating=2).count()
        rate_system['star3'] = product_comments.filter(rating=3).count()
        rate_system['star4'] = product_comments.filter(rating=4).count()
        rate_system['star5'] = product_comments.filter(rating=5).count()
        return(rate_system)

    def review_user_check():
        user_comment = ''
        if request.user.is_authenticated:
            user_comment = product_comments.filter(user_id=request.user)
        return user_comment

    if request.user.is_authenticated:
        comments = product_comments.filter(~Q(user_id=request.user))
    else:
        comments = product_comments.all()

    context = {
        'product': product,
        'category_name': category_name,
        'store_name': store_name,
        'store_slug': store_slug,
        'store_type_name': store_type_name,
        'store_type_slug': p_store_type,
        'store_categories': store_categories(store_name),
        'similar_products': similar_products,
        'product_comments': comments[:3],
        'product_comments_count': product_comments_count,
        'overall_rating': overall_rating(),
        'rating_system': rating_system(),
        'user_comment': review_user_check(),
    }
    if request.user.is_authenticated:
        check_user = request.user
    else:
        check_user = ''
    context.update(needed_everywhere(check_user))
    return render(request, 'core/product_details.html', context)


@ login_required(login_url='/accounts/login/')
def favourite_product(request, slug):

    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(core_models.Product, slug=slug)
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
        messages.warning(
            request, f'"{product.name}" has been removed from your wishlist.')
    else:
        product.favourite.add(request.user)
        messages.success(
            request, f'"{product.name}" has been added to your wishlist.')
    return HttpResponseRedirect(url)


@ login_required(login_url='/accounts/login/')
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
    product_name = core_models.Comment.objects.filter(
        user_id=current_user.id, product_id=id)[0]
    print(product_name)
    messages.success(
        request, f'Your comment on "{product_name.product.name}" have been added successfully.')
    return HttpResponseRedirect(url)


@ login_required(login_url='/accounts/login/')
def delete_comment(request, proid):

    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    product_name = core_models.Comment.objects.filter(
        user_id=current_user.id, id=proid)[0]
    core_models.Comment.objects.filter(
        user_id=current_user.id, id=proid).delete()
    messages.warning(
        request, f"Your comment on '{product_name.product.name}' has been deleted.")
    return HttpResponseRedirect(url)


class SearchView(ListView):

    template_name = 'core/products_list.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        return self.get_queryset()

    def get_queryset(self):
        search_term = self.request.GET.get('q').strip(' */%^$#@!?')
        products = core_models.Product.objects.filter(Q(name__icontains=search_term) | Q(
            category__name__icontains=search_term) | Q(brand__name__icontains=search_term) | Q(description__icontains=search_term))
        products_number = products.count()
        current_url = resolve(self.request.path_info).url_name
        context = {
            'store_products': products,
            'products_number': products_number,
            'search': search_term,
            'url_name': current_url,
            'products_paginator': paginate_view(self.request, products),
            'search_exist': 'true',
        }
        if self.request.user.is_authenticated:
            check_user = self.request.user
        else:
            check_user = ''
        context.update(needed_everywhere(check_user))
        return context


def reviews_list(request, pr_store_type, store_slug, category_slug, slug):
    product_slug = core_models.Product.objects.filter(slug__iexact=slug)
    name = check_on_slug(product_slug)
    if name is None:
        return HttpResponse('<h1>Post Not Found</h1>')

    product = name
    category_name = product.category.name
    store_name = product.category.store.name
    store_type_name = product.category.store.storetype.name
    product_comments = core_models.Comment.objects.filter(
        product__name=product).order_by('-create_at')
    product_comments_count = product_comments.count()

    def overall_rating():
        if product_comments:
            sum, count = 0, 0
            for comment in product_comments:
                sum += comment.rating
                count += 1
        else:
            return 0
        return(round(sum/count, 1))

    def rating_system():
        rate_system = {}
        count = 0
        rate_system['star1'] = product_comments.filter(rating=1).count()
        rate_system['star2'] = product_comments.filter(rating=2).count()
        rate_system['star3'] = product_comments.filter(rating=3).count()
        rate_system['star4'] = product_comments.filter(rating=4).count()
        rate_system['star5'] = product_comments.filter(rating=5).count()
        return(rate_system)

    def review_user_check():
        user_comment = ''
        if request.user.is_authenticated:
            user_comment = product_comments.filter(user_id=request.user)
        return user_comment

    if request.user.is_authenticated:
        comments = product_comments.filter(~Q(user_id=request.user))
    else:
        comments = product_comments.all()

    context = {
        'product': product,
        'category_name': category_name,
        'store_name': store_name,
        'store_slug': store_slug,
        'store_type_name': store_type_name,
        'store_type_slug': pr_store_type,
        'store_categories': store_categories(store_name),
        'product_comments': comments,
        'product_comments_count': product_comments_count,
        'overall_rating': overall_rating(),
        'rating_system': rating_system(),
        'reviews_page': 'true',
        'user_comment': review_user_check(),
    }
    if request.user.is_authenticated:
        check_user = request.user
    else:
        check_user = ''
    context.update(needed_everywhere(check_user))
    return render(request, 'core/reviews_list.html', context)


# extra
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


def needed_everywhere(check_user):
    context = {}
    all_products = {}
    all_stores = core_models.Store.objects.all().order_by('-create_at')
    if check_user:
        current_user = check_user
        total = 0
        count_cart = 0
        cart = order_models.ShopCart.objects.filter(user_id_id=current_user)
        for product in cart:
            total += product.amount
            count_cart += 1

        context['cart'] = cart
        context['total'] = total
        context['count_cart'] = count_cart
        context['owner'] = account_models.OwnerProfile.objects.filter(
            user=check_user)

    for store in all_stores:
        all_products[store.name] = core_models.Product.objects.filter(
            category__store__name=store.name).order_by('-create_at')[:12]

    context['all_stores'] = all_stores
    context['all_products'] = all_products
    context['all_category'] = core_models.Category.objects.all()
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


def Quick_View (request):
    current_user = request.user
    
    if request.is_ajax():
        
        name_product = request.GET.get("product_name")
        
        product = core_models.Product.objects.filter(name = name_product)
        product_id = product[0].id

        product_name = product[0].name
        image =product[0].image
        description = product[0].description
        price = product[0].price
        discount_price=product[0].discount_price
        color = product[0].color
        size = product[0].size
        c_store_type = product[0].category.store.storetype.slug
        category_slug = product[0].category.slug
        slug=product[0].slug
        store_slug = product[0].category.store.slug
        fav = product[0].favourite.all()

        if  current_user in fav:
           favourite =True
        else:
            favourite = False   

        slug_product = ("/{c_store_type}-type/{store_slug}/{category_slug}/{slug}/").format(c_store_type=c_store_type, store_slug=store_slug, category_slug=category_slug, slug=slug)

        favourite_slag = ('/favourite-product/{slug}/').format(slug = slug)
        add_product_herf = ('/order/addtoshpcart/{id}/').format(id = product_id )
        image = str(image)
        slug_product = str(slug_product)
        
        context = {
                'product_name': product_name,
                'image': image,
                'description':description,
                'price': price,
                'discount_price': discount_price,
                'color': color,
                'size': size,
                'slug':slug_product,
                'id':product_id,
                'favourite': favourite,
                'favourite_slag':favourite_slag,
                'add':add_product_herf,


            }
        return JsonResponse(context)



 