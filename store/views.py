import json, uuid
import itertools 
from datetime import datetime
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from .forms import AddProductForm, OrderItemForm, BillingForm, ReviewForm, UpdateProductForm
from Accounts.models import Vendor, User, Customer
from store.models import Product, Order, OrderItem, Review, UsersRecentlyViewedProduct, WishList
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import attrgetter
# Create your views here.

import phonenumbers
from faker.providers.phone_number.en_US import Provider

class CustomPhoneProvider(Provider):
    def phone_number(self):
        while True:
            phone_number = self.numerify(self.random_element(self.formats))
            parsed_number = phonenumbers.parse(phone_number, 'US')
            if phonenumbers.is_valid_number(parsed_number):
                return phonenumbers.format_number(
                    parsed_number,
                    phonenumbers.PhoneNumberFormat.E164
                )

class ShopView(TemplateView):
    template_name = 'shop.html'


class ContactView(TemplateView):
    template_name = 'contact.html'

def men_category(request):
    return render(request, 'store/categories/men.html')

def pagination(request, items_list, num_of_pages):
    page_number = request.GET.get('page', 1)
    products_paginator = Paginator(items_list, num_of_pages)
    try:
        productss = products_paginator.page(page_number)
    except PageNotAnInteger:
        productss = products_paginator.page(1)
    except EmptyPage:
        productss = products_paginator.page(products_paginator.num_pages)
    return productss


def add_product_view(request):
    """The view for vendors to add products to the store"""
    user = request.user

    if not user.is_authenticated:
        return redirect('user:login')

    context = {}
    
    if request.method == "POST":
        add_form = AddProductForm(request.POST, request.FILES)
        
        if add_form.is_valid():
            obj = add_form.save(commit=False)
            # seller = Vendor.objects.filter(emaVendoril=request.user.email).first()
            obj.seller = request.user
            obj.save()
            messages.success(request, 'Product has been added to store.')
        # else:
        #     return HttpResponse('buggy')
        else:
            messages.error(request, 'Product was not added due to an error.')
            

    else:
        add_form = AddProductForm()
    context['add_product_form'] = add_form
    return render(request,'store/create_product.html',context)

def vendor_dashboard(request):
    vendors = Vendor.objects.all()
    if not request.user.is_authenticated:
        return HttpResponse('You must be authorized to visit this page.')
    for vendor in vendors:
        if vendor.username != request.user.username:
            return HttpResponse('You cannot access this page because you are not the vendor of this product.')
    
    vendor_username = request.user.username
    vendor = Vendor.objects.get(username=vendor_username)
    vendor_products = Product.objects.filter(seller=vendor)
    completed_order_products = OrderItem.objects.filter(order__complete=True)
    uncompleted_order_products = OrderItem.objects.filter(order__complete=False)
    return render(request, 'store/vendor_dashboard.html', {'vendor_products': vendor_products, 'completed_order_products': completed_order_products, 'uncompleted_order_products': uncompleted_order_products})

def customer_dashboard(request):
    customers = Customer.objects.all()
    vendors = Vendor.objects.all()
    if not request.user.is_authenticated:
        return redirect('user:must_auth')
    for vendor in vendors:
        if vendor.username == request.user.username:
            return HttpResponse("You must create a Customer Account to be able to access customers' privileges.")
    completed_orders = OrderItem.objects.filter(order__customer__username=request.user.username, order__complete=True)
    
    uncompleted_orders = OrderItem.objects.filter(order__customer__username=request.user.username, order__complete=False)
    

    return render(request, 'store/customer_dashbord.html', {'completed_orders': completed_orders, 'uncompleted_orders': uncompleted_orders})

def home_page(request):
    context = {}
    val = ''
    customers = Customer.objects.all()
    vendors = Vendor.objects.all()
    if request.user.is_authenticated:
        for c in customers:
            if c.email == request.user.email:
                val = 'customer'
        for c in vendors:
            if c.email == request.user.email:
                val = 'vendor'
        context['val'] = val
    products = Product.objects.all().order_by('?').distinct()[:6]
    latest_products = Product.objects.all().order_by('-product_id')

    # products1 = sorted(get_product_queryset(request), key=attrgetter('product_id'), reverse=True)
    # products_list = Product.objects.all()
    recently_added_products = Product.objects.all()
    productss = pagination(request, latest_products, 8)
    context['p_products'] = productss
    context['products'] = pagination(request, Product.objects.all().order_by('-num_of_visits'), 6)
    context['latest_products'] = sorted(recently_added_products, key=attrgetter('date_added'), reverse=True)[:6]
    return render(request, 'store/index.html', context)

def just_arrived(request):
    context = {}
    products = Product.objects.all()

    context['latest_products'] = pagination(request, sorted(products, key=attrgetter('date_added'), reverse=True), 9)
    return render(request, 'store/just_arrived.html', context)

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        user = User.objects.get(device=request.session.get('device'))
        customer = Customer.objects.get(device=user.device)
    else:
        try:
            customer = Customer.objects.get(username=request.user.username)
        except ObjectDoesNotExist:
            return HttpResponse("You must create a Customer Account to be able to access customers' privileges.")
    product = Product.objects.get(product_id=product_id)
    
    try:    
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    except:
        order = Order.objects.filter(customer=customer).order_by('-id').first()
    # orderitems = []
    orderitem, created = OrderItem.objects.get_or_create(product=product, order=order, color=request.POST.get('color'), size=request.POST.get('size'))
    orderitems = OrderItem.objects.filter(product=product, order=order)
    COLOR_CHOICES = []
    SIZE_CHOICES = []
    for color in product.product_colors.split(','):
        color = color.strip()
        COLOR_CHOICES.append((color, color))
        # order_item.save()
    for size in product.product_sizes.split(','):
        size = size.strip()
        SIZE_CHOICES.append((size, size))
    if request.method == 'POST':
        
        orderitemform = OrderItemForm(data=request.POST, size_choices=SIZE_CHOICES, color_choices=COLOR_CHOICES)

        if orderitemform.is_valid():
            
            # obj = orderitemform.save(commit=False)
            
            # elif orderitemform.cleaned_data['color'] == orderitem.color:
            #     orderitem.quantity += orderitemform.cleaned_data['quantity']
            # else:
            #     orderitem.color = orderitemform.cleaned_data['color']
            sum_qty = 0
            for i in OrderItem.objects.filter(order=order, product=product):
                sum_qty += i.quantity
            sum_qty = orderitemform.cleaned_data['quantity'] + sum_qty
            # 
            if orderitem.product.number_available == 0:
                messages.info(request, 'Product is out of stock.')
            if orderitemform.cleaned_data['quantity'] > orderitem.product.number_available and orderitem.product.number_available != 0:
                orderitem.quantity += 0
                messages.error(request, 'Quantity more than available product.')
                OrderItemForm(size_choices=SIZE_CHOICES, color_choices=COLOR_CHOICES)
            if orderitemform.cleaned_data['quantity'] < orderitem.product.number_available:
                if sum_qty <= orderitem.product.number_available:
                    if orderitem.size == orderitemform.cleaned_data['size'] and orderitemform.cleaned_data['color'] == orderitem.color:
                        orderitem.quantity += orderitemform.cleaned_data['quantity']
                    else:
                        OrderItem.objects.create(order=order, product=product, color=orderitemform.cleaned_data['color'], size=orderitemform.cleaned_data['size'], quantity=orderitemform.cleaned_data['quantity'])
                    # if orderitemform.cleaned_data['size'] != OrderItem.objects.filter(order=order, product=product).last().size or orderitemform.cleaned_data['color'] != OrderItem.objects.filter(order=order, product=product).last().color:
                    #     OrderItem.objects.create(order=order, product=product, color=orderitemform.cleaned_data['color'], size=orderitemform.cleaned_data['size'], quantity=orderitemform.cleaned_data['quantity'])
                        
                    # elif orderitemform.cleaned_data['size'] == OrderItem.objects.filter(order=order, product=product).last().size or orderitemform.cleaned_data['color'] == OrderItem.objects.filter(order=order, product=product).last().color:
                    #     orderitem.quantity += orderitemform.cleaned_data['quantity']
                    
                    messages.success(request, 'Item has been added to Cart.')
            elif orderitemform.cleaned_data['quantity'] <= 0:
                orderitem.quantity += 0
                messages.error(request, 'You must add at least one item.')
            orderitem.date_added = datetime.now()
            orderitem.save()
    else:
        orderitemform = OrderItemForm(size_choices=SIZE_CHOICES, color_choices=COLOR_CHOICES)

    if orderitem.quantity <= 0:
        orderitem.quantity = 0
    orderitem.date_added = datetime.now()
    orderitem.save()
    context = {
        'product': product,
        'orderitemform': orderitemform,
    }
    # if True:
    #     return redirect('home')
    return render(request, 'store/detail.html', context)

def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('user:must_auth')
    
    product = Product.objects.get(product_id=product_id)
    customer = Customer.objects.get(email=request.user)
    # try:
    wish_item = WishList.objects.filter(product=product, customer=customer)
    if wish_item.count() > 0:
        bool = False
    else:
        wish_item = WishList.objects.create(product=product, customer=customer, heart_val=1, date_added=datetime.now())
        bool = True
    
    return JsonResponse(bool, safe=False)

def remove_from_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('user:must_auth')
    
    product = Product.objects.get(product_id=product_id)
    customer = Customer.objects.get(email=request.user)
    wish_item = WishList.objects.get(product=product, customer=customer)
    wish_item.delete()
    bool = True
    return HttpResponse('OK.')

def remove_from_wishlist_view(request, product_id):
    if not request.user.is_authenticated:
        return redirect('user:must_auth')
    
    product = Product.objects.get(product_id=product_id)
    customer = Customer.objects.get(email=request.user)
    wish_item = WishList.objects.get(product=product, customer=customer)
    wish_item.delete()
    # if True:
    return redirect('wishlist')
    # return render(request, 'store/wishlist.html')

def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('user:must_auth')
    wishlist = WishList.objects.filter(customer=request.user)

    return render(request, 'store/wishlist.html', {'wishlist': wishlist})
def cart(request):
    context = {}

    if request.user.is_authenticated:
        try:
            user = Customer.objects.get(username=request.user.username)
        except ObjectDoesNotExist:
            return HttpResponse("You must create a Customer Account to be able to access customers' privileges.")
    else:
        user = Customer.objects.get(device=request.session.get('device'))
    # try:
    
    # 
    
    
    if Order.objects.filter(customer=user).order_by('-id').first() is not None:
        if Order.objects.filter(customer=user).order_by('-id').first().get_cart_total == 0:
            
            return redirect('no_cart')
    else:
        return redirect('home')
    # order, created = Order.objects.get_or_create(customer=user, complete=False)
    try:    
        order, created = Order.objects.get_or_create(customer=user, complete=False)
        
    except:
        order = Order.objects.filter(customer=user).order_by('-id').first()
        
    # if order.complete == False:
    items = order.orderitem_set.all()
    for item in items:
        if item.quantity <= 0 or item.product.number_available == 0:
            order.get_cart_total -= item.get_items_price
            order.save()
            item.delete()
        if item.quantity > item.product.number_available:
            item.quantity = item.product.number_available
            item.save()

    if len(items) == 0:
        
        order.total_order_price = 100
        order.save()
        # 
        
        return redirect('no_cart')
    else:
        
        order.total_order_price = order.get_cart_total + 100
        subtotal = order.get_cart_total
        order.save()
        total = order.total_order_price

    context['sub_total'] = subtotal
    context['total'] = total
    context['order'] = order
    context['items'] = items

    return render(request, 'store/cart.html', context)


def quantity_increment(request, item_id):
    order_item = OrderItem.objects.get(item_id=item_id)
    if order_item.quantity < order_item.product.number_available:
        order_item.quantity += 1
        
    else:
        order_item.quantity = order_item.product.number_available
    order_item.save()
    subtotal = order_item.order.get_cart_total
    total = subtotal + 100
    i = 1
    if i == 1:
        return redirect('cart')
    return render(request, 'store/cart.html', {'sub_total':subtotal, 'total':total})
    

def quantity_decrement(request, item_id):

    try:
        order_item = OrderItem.objects.get(item_id=item_id)
    except ObjectDoesNotExist:
        # order_item.delete()
        return redirect('cart')
    else:
        if order_item.quantity <=  0:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        i = 1
        if i == 1:
            return redirect('cart')
        subtotal = order_item.order.get_cart_total
        total = subtotal + 100
    return render(request, 'store/cart.html', {'sub_total':subtotal, 'total':total})


def delete_order_item(request, item_id):
    order_item = OrderItem.objects.get(item_id=item_id)
    o = order_item
    subtotal = order_item.order.get_cart_total - order_item.get_items_price
    total = subtotal + 10
    order_item.delete()
    i = 1
    if i == 1:
        return redirect('cart')

    return render(request, 'store/cart.html', {'sub_total':subtotal, 'total':total})



def checkout(request):
    context = {}
    user = request.user

    if not user.is_authenticated:
        return redirect('user:must_auth')
    if request.user not in Customer.objects.all():
        return HttpResponse("You must create a Customer Account to be able to access customers' privileges.")

    order = Order.objects.filter(customer=user).order_by('-id').first()
    if order is not None:
        if Order.objects.filter(customer=user).order_by('-id').first().get_cart_total == 0:
            return redirect('no_checkout')
        else:
            if request.method == 'POST':
                billing_form = BillingForm(request.POST)
                if billing_form.is_valid():
                    
                    obj = billing_form.save(commit=False)
                    # obj.phone_num1 = billing_form.cleaned_data['phone_num1']
                    # obj.fullname = billing_form.cleaned_data['fullname']
                    # obj.email = billing_form.cleaned_data['email']
                    # obj.address = billing_form.cleaned_data['address']
                    # obj.country = billing_form.cleaned_data['country']
                    # obj.city = billing_form.cleaned_data['city']
                    # obj.state = billing_form.cleaned_data['state']
                    # obj.zipcode = billing_form.cleaned_data['zipcode']
                    
                    

                    obj.customer = Customer.objects.get(username=request.user.username)
                    obj.order = Order.objects.filter(customer=user).order_by('-id').first()
                    obj.order.date_ordered = datetime.now()
                    # obj.order.complete = not obj.order.complete
                    
                    obj.order.save()
                    obj.save()
                    # order.complete = 

                    # items = OrderItem.objects.filter(order=obj.order)
                    # for item in items:
                    #     item.product.number_available -= item.quantity
                    #     item.product.save()
                    # billing_form= obj
                    # messages.success(request, 'Your order has been placed. Thank you for patronizing us!')
                    return redirect('wallet:make-payment')
                    # make_payment(request)
                else:
                    messages.error(request, 'Unable to checkout.')
            else:
                billing_form = BillingForm()

            try:    
                order, created = Order.objects.get_or_create(customer=user, complete=False)
            except:
                order = Order.objects.filter(customer=user).order_by('-id').first()
            # order = Order.objects.filter(customer=user).order_by('-id').first()
            items = order.orderitem_set.all()
            
            
            if len(items) == 0:
                return redirect('no_checkout')
            else:
                subtotal = order.get_cart_total
                total = order.total_order_price
        

            context['sub_total'] = subtotal
            context['total'] = total
            context['billing_form'] = billing_form
            context['order'] = order
            context['items'] = items

    else:
        return redirect('no_checkout')

    
    return render(request, 'store/checkout.html', context)


def no_cart(request):
    return render(request, 'store/no_cart.html')

def no_checkout(request):
    return render(request, 'store/no_checkout.html')


def review(request, product_id):
    product = Product.objects.get(product_id=product_id)
    if not request.user.is_authenticated:
        messages.info(request, 'You must be logged in to leave reviews/ratings.')
        return redirect('product_details', product_id)
    customer = User.objects.get(email=request.user.email)
    # except ObjectDoesNotExist:
    #     return HttpResponse('You must be a customer to access this page')
    # reviews = product.review_set.all()
    
    if request.method == 'GET':
        review_form = ReviewForm(request.GET)
        if review_form.is_valid():
            if OrderItem.objects.filter(order__customer__username=request.user.username, product__product_id=product_id, order__complete=True):
                obj = review_form.save(commit=False)
                obj.product = product
                obj.user = customer
                obj.rating = request.GET.get('rating')
                if obj.user_review == '':
                    messages.error(request, "Your comment can't be blank.")
                    return redirect('product_details', product.product_id)
                else:
                    messages.success(request, 'Your review has been posted.')
                obj.save()
                return redirect('product_details', product.product_id)
            else:
                messages.info(request, 'You have not ordered this product. Therefore you cant make comments.')
        else:
            messages.error(request, 'An error was found in the form.')
            
    else:
        review_form = ReviewForm()
    return render(request, 'store/detail.html', {'review_form': review_form, 'product': product})

def product_details(request, product_id):
    context = {}
    if not request.user.is_authenticated:
        messages.info(request, 'Note: You must be logged in to add items to your WishList.')
    product = get_object_or_404(Product, product_id=product_id)
    try:
        context['heart_val'] = heart_val = WishList.objects.get(product=product, customer=request.user).heart_val
    except:
        pass
    reviews = product.review_set.all()
    reviews = sorted(reviews, key=attrgetter('created_on'), reverse=True)
    reviews_counter = 0
    reviews_rating_sum_counter = 0
    reviews_rating_counter = 0
    for review in reviews:
        reviews_counter+=1
        reviews_rating_counter += 1
        if review.rating is not None:
            reviews_rating_sum_counter += review.rating
        else:
            reviews_rating_sum_counter += 0
    product.num_of_reviews = reviews_counter
    product.num_of_ratings = reviews_rating_counter
    if product.num_of_visits is not None:
        product.num_of_visits += 1
    else:
        product.num_of_visits = 1
    try:
        product.average_rating = int(reviews_rating_sum_counter/product.num_of_ratings)
    except:
        product.average_rating = 0
    product.save()
    reviews_counter = product.num_of_reviews
    
    if not request.user.is_authenticated:
        user = User.objects.get(device=request.session.get('device'))
        customer = Customer.objects.get(device=user.device)
    else:
        try:
            customer = Customer.objects.get(username=request.user.username)
        except ObjectDoesNotExist:
            return HttpResponse("You must create a Customer Account to be able to access customers' privileges.")
    product.customer_viewed_by = customer
    product.save()
    user_viewed = UsersRecentlyViewedProduct.objects.create(
        customer = customer,
        product = product,
        time_visited = datetime.now()
    )
    try:
        order_item, created = OrderItem.objects.get_or_create(product=product, order__customer__email=request.user.email)
    except:
        order_item, created = OrderItem.objects.get_or_create(product=product, order__customer__device=request.session.get('device'))
    
    users_recently_viewed_products = UsersRecentlyViewedProduct.objects.filter(customer=customer).order_by('-time_visited').values('product').distinct()
    users_recently_viewed_products = Product.objects.filter(product_id__in=users_recently_viewed_products, customer_viewed_by=customer).order_by('-last_visit')
    for i in users_recently_viewed_products:
        if i.product_id == product_id:
            users_recently_viewed_products
    # try:
    #     request.session.get['p_id']
    # except:
    #     request.session['p_id'] = product_id
    
    COLOR_CHOICES = []
    SIZE_CHOICES = []
    for color in order_item.ordered_product_color:
        color = color.strip()
        COLOR_CHOICES.append((color, color))
        # order_item.save()
    for size in order_item.ordered_product_size:
        size = size.strip()
        SIZE_CHOICES.append((size, size))

    orderitemform = OrderItemForm(SIZE_CHOICES, COLOR_CHOICES)
    product_sizes = product.product_sizes.split(',')
    product_colors = product.product_colors.split(',')
    
    context['product'] = product
    context['productss'] = Product.objects.all()
    context['product_sizes'] = product_sizes
    context['product_colors'] = product_colors
    context['orderitemform'] = orderitemform
    context['reviews'] = pagination(request, reviews, 5)
    context['reviews_counter'] = reviews_counter
    context['users_recently_viewed_products'] = users_recently_viewed_products[:4]
    return render(request, 'store/detail.html', context)

def vendor_product_detail(request, product_id):
    vendors = Vendor.objects.all()
    if not request.user.is_authenticated:
        return HttpResponse('You must be authorized to visit this page.')
    for vendor in vendors:
        if vendor.username != request.user.username:
            return HttpResponse('You cannot access this page because you are not the vendor of this product.')
    product = Product.objects.get(product_id=product_id)
    reviews = product.review_set.all()
    reviews = sorted(reviews, key=attrgetter('created_on'), reverse=True)
    return render(request, 'store/vendor_product_detail.html', {'product': product, 'reviews': pagination(request, reviews, 3)})

def get_product_queryset(request):
    """The view that performs the search functionality"""
    if request.method == 'GET':
        query = request.GET.get('query', '')
        

        if query is not None:
            products = Product.objects.filter(
                Q(product_name__icontains=query) | Q(product_description__icontains=query) | Q(product_categories__icontains=query)
            ).distinct()
            
            if not products:
                return HttpResponse('No search result for this query.')
            
            productss = pagination(request, products, 3)
            context = {
                'results': productss,
                'query': str(query)
            }

            return render(request, 'store/index.html', context)
        else:
            return render(request, 'store/index.html')
    else:
        return render(request, 'store/index.html')

def update_product(request, product_id):
    product = Product.objects.get(product_id=product_id)
    vendors = Vendor.objects.all()
    if not request.user.is_authenticated:
        return HttpResponse('You must be authorized to visit this page.')
    for vendor in vendors:
        if vendor.username != request.user.username:
            return HttpResponse('You cannot access this page because you are not the vendor of this product.')
    if request.method == 'POST':
        update_product_form = UpdateProductForm(request.POST or None, request.FILES or None, instance=product)
        if update_product_form.is_valid():
            update_product_form.save()
            messages.success(request, 'The product has been updated.')
        else:
            messages.error(request, 'There was error in the form.')
    update_product_form = UpdateProductForm(instance=request.user, initial= {
        "product_name": product.product_name,
        "product_description": product.product_description,
        "product_colors": product.product_colors,
        "product_sizes": product.product_sizes,
        "product_categories": product.product_categories,
        "product_price": product.product_price,
        "number_available": product.number_available,
        "product_image1": product.product_image1,
        "product_image2": product.product_image2,
        "product_image3": product.product_image3,
        }
    )
    return render(request, 'store/update_product.html', {'product': product, 'update_product_form': update_product_form,})

def delete_product(request, product_id):
    product = Product.objects.get(product_id=product_id)
    product.delete()
    return redirect('v_dashboard')

