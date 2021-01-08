from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from order.models import ShopCart, ShopCartForm, OrderForm, OrderDetail, Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from account import forms as account_forms
from account import models as account_models
from core import views as core_views
from core import models as core_models
from datetime import datetime, timedelta


@login_required(login_url='/accounts/login/')
def addtoshpcart(request,id):
    url = request.META.get('HTTP_REFERER') # GET LAST URL
    current_user = request.user # access user session information
    controller = True
    checkproduct = ShopCart.objects.filter(product_cart_id=id, user_id = current_user)
    print(checkproduct)
   
    if checkproduct :
        control = 1
    else:
        control = 0

    if request.method == 'POST':
        form = ShopCartForm(request.POST)

        
        if form.is_valid():
            color = form.cleaned_data['color_Choiced']
            size =  form.cleaned_data['size_Choiced']
            print(color)
            print(size)

            if control ==1:
                data1 = ShopCart.objects.filter(product_cart_id =id,user_id = current_user )
                for data in data1:
                    if data.color_Choiced == color and data.size_Choiced == size:
                        data.quantity+= form.cleaned_data['quantity']
                        controller = False
                        data.save()
                        
                if controller:
                    data = ShopCart()
                    data.user_id_id = current_user.id 
                    data.product_cart_id = id 
                    data.size_Choiced = form.cleaned_data['size_Choiced']
                    data.color_Choiced = form.cleaned_data['color_Choiced']
                    data.quantity = form.cleaned_data['quantity']
                    data.save()    
            else:
                data = ShopCart()
                data.user_id_id = current_user.id 
                data.product_cart_id = id 
                data.size_Choiced = form.cleaned_data['size_Choiced']
                data.color_Choiced = form.cleaned_data['color_Choiced']
                data.quantity = form.cleaned_data['quantity']

                data.save()   

    
        messages.success(request,"Product added to Shpcart")
        return HttpResponseRedirect(url)

    else:
        if control ==1:
            data1 = ShopCart.objects.filter(product_cart_id =id, user_id = current_user)

            for data in data1 :
                if not data.color_Choiced and not data.size_Choiced:
                    data.quantity +=1
                    data.save()
                    controller = False
            if controller:
                data = ShopCart()
                data.user_id_id = current_user.id 
                data.product_cart_id = id 
                data.quantity = 1
                data.save() 
        else: 
            data = ShopCart()
            data.user_id_id = current_user.id 
            data.product_cart_id = id 
            data.quantity = 1
            data.save()   
    messages.success(request,"Product added to Shpcart")
    return HttpResponseRedirect(url)


@login_required(login_url='/accounts/login/')
def shopcart(request):
    current_user = request.user
    total = 0

    cart = ShopCart.objects.filter(user_id_id=current_user)
    form = account_forms.ProfileUpdateForm(instance=request.user)

    userInfo = account_models.UserRegistration.objects.filter(
        username=request.user.username)[0]
    for product in cart:
        total += product.amount

    context = {'cart': cart,
               'total': round(total,2),
               'form': form,
               'userInfo':  userInfo, }

    context.update(core_views.needed_everywhere(request.user))
    return render(request, 'order/cart.html', context)


@login_required(login_url='/accounts/login/')
def deletefromcart(request, id):
    print('id')
    url = request.META.get('HTTP_REFERER')
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "item deleted ")
    return HttpResponseRedirect(url)


@login_required(login_url='/accounts/login/')
def updatefromcart(request, id):
    controller = True
    # if this is a POST request we need to process the form data
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():  # check whether it's valid:

            # get product quantity from form
            quantity = form.cleaned_data['quantity']
            color = form.cleaned_data['color_Choiced']
            size = form.cleaned_data['size_Choiced']
            current_user = request.user  # Get User id
            product = ShopCart.objects.get(
                user_id_id=current_user.id,id=id)

            if product.product_cart.color or product.product_cart.size:
                if product.color_Choiced == color and  product.size_Choiced == size:
                    new_quantity = quantity - product.quantity
                    product.quantity = product.quantity + new_quantity
                    controller = False
                    product.save()

                else:

                    data1 = ShopCart.objects.filter(product_cart_id =product.product_cart.id, user_id = current_user)
                    for data in data1:
                        if data.color_Choiced == color and data.size_Choiced == size:
                            data.quantity+= form.cleaned_data['quantity']
                            controller = False
                            data.save()
                            ShopCart.objects.filter(id=id).delete()
                        
                    if controller:
                        data = ShopCart()
                        data.user_id_id = current_user.id 
                        data.product_cart_id = product.product_cart.id 
                        data.size_Choiced = form.cleaned_data['size_Choiced']
                        data.color_Choiced = form.cleaned_data['color_Choiced']
                        data.quantity = form.cleaned_data['quantity']
                        ShopCart.objects.filter(id=id).delete()
                        data.save()




            elif product != None:  # Update  quantity to exist product quantity
                    new_quantity = quantity - product.quantity
                    product.quantity = product.quantity + new_quantity
                    product.save()
            
            messages.success(
                request, f"{product.product_cart.name}  has been updated.")
                
    return HttpResponseRedirect(url)


@login_required(login_url='/users/login')
def checkout(request):

    current_user = request.user
    shopcart = ShopCart.objects.all().filter(user_id=current_user.id)

    total_cart = 0
    new_date = datetime.today() + timedelta(2)

    for product in shopcart:
        total_cart += product.amount  
    context = {}
    if request.method == 'POST':
        form = OrderForm(request.POST or None)

        # check whether it's valid:
        if form.is_valid():

            data = Order()
            # get product quantity from form
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.note = form.cleaned_data['note']
            data.email = current_user.email
            data.user_id = current_user.id
            data.total = total_cart
            data.save()

            # Save Shopcart items to Order detail items
            
            for product in shopcart:
                detail = OrderDetail()
                detail.order_id = data.id  # Order Id
                detail.product_id = product.product_cart.id
                detail.user_id = current_user.id
                detail.quantity = product.quantity
                detail.deliver_time = new_date

                if product.product_cart.discount_price:
                    detail.price = product.product_cart.discount_price
                else:
                    detail.price = product.product_cart.price

                detail.total = detail.price * product.quantity
                    
                if product.size_Choiced:
                    detail.size_Choiced = product.size_Choiced
                
                if product.color_Choiced:
                    detail.color_Choiced = product.color_Choiced


                
                detail.save()
               

            order_details = Order.objects.filter(user_id=current_user.id).order_by('-create_at')[0]
            context={'details':order_details,
                      'order_id':data.id ,     }
            context.update(core_views.needed_everywhere(request.user))
            return render(request,"order/checkout_review.html",context )


    # context.update(views.total_price_items(request.user.id))
    return render(request, 'order/cart.html')


@login_required(login_url='/users/login')
def checkout_complete(request, id):
    current_user = request.user

    order_details = Order.objects.filter(id=id)[0]
    order_product_details = OrderDetail.objects.filter(order_id=id)
    total = 0
    for subtotal in order_product_details:
        total += subtotal.total
    # profiles = users_models.Profile.objects.filter(user_id=request.user.id)
    context = {
        'order_details': order_details,
        'order_product_details': order_product_details,
        'total_order': round(total,2),
        
    }
    # context.update(views.total_price_items(request.user.id))

    # Clear & Delete shopcart
    ShopCart.objects.filter(user_id_id=current_user.id).delete()
    messages.success(
        request, f"Thank for Providing Your Info, Mr.{request.user.username}. Your order has been completed. We will contact with you based on your info below.")
    return render(request, "order/complete_checkout.html", context)


@login_required(login_url='/users/login')
def checkout_delete(request, id):
    context = {'id': id}
    Order.objects.filter(id=id).delete()
    OrderDetail.objects.filter(order_id=id).delete()
    context.update(core_views.needed_everywhere(request.user))
    messages.success(
        request, f" Mr.{request.user.username}. Your order will be deleted. do you want to continue .")
    return redirect("order:shopcart")


