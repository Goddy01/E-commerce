"""E_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import template
from django.contrib import admin
from django.urls import path, include, reverse_lazy,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from store.views import (
    delete_order_item, home_page, ContactView,
    ShopView, product_details,
    cart, checkout,
    add_product_view, quantity_increment,
    quantity_decrement, delete_order_item,
    # load_cities,
    no_cart, all_reviews,
    no_checkout, add_to_cart,
    get_product_queryset, review,
    vendor_dashboard, delete_product,
    vendor_product_detail, update_product,
    customer_dashboard, just_arrived,
    add_to_wishlist, remove_from_wishlist,
    wishlist, remove_from_wishlist_view,
    men_category,women_category,
    male_children_category, female_children_category,
    no_search, billing_address,
    make_payment, shop
    )
urlpatterns = [
    path('admin/', admin.site.urls),
    path("paystack", include(("paystack.frameworks.django.urls", 'paystack'),namespace='paystack')),
    path('', home_page, name='home'),
    path('shop/', shop, name='shop'),
    path('make-payment/', make_payment, name='make-payment'),
    path('add_to_cart/<product_id>/', add_to_cart, name='add_to_cart'),
    path('just_arrived_products/', just_arrived, name='just_arrived'),
    path('add_to_wishlist/<product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    # path('shop/', ShopDetailView.as_view(), name='shop'),
    path('<product_id>/product_details/', product_details, name='product_details'),
    path('wishlist/', wishlist, name='wishlist'),
    path('remove_from_wishlist_view/<product_id>', remove_from_wishlist_view, name='remove_from_wishlist_view'),
    path('search/', get_product_queryset, name="search"),
    path('no-search/', no_search, name="no_search"),
    path('<product_id>/reviews/', review, name="review"),
    path('vendor_dashboard/', vendor_dashboard, name='v_dashboard'),
    path('customer_dashboard/', customer_dashboard, name='c_dashboard'),
    path('billing_address/<transaction_id>/', billing_address, name='billing_address'),
    path('<product_id>/vendor_product_details/', vendor_product_detail, name='v_product_details'),
    path('<product_id>/update_product', update_product, name="update_product"),
    path('<product_id>/delete_product', delete_product, name="delete_product"),
    path('cart/', cart, name='cart'),
    path('all_reviews/<product_id>/', all_reviews, name='all_reviews'),
    path('men_category/', men_category, name='men_category'),
    path('women_category/', women_category, name='women_category'),
    path('male_children_category/', male_children_category, name='male_children_category'),
    path('female_children_category/', female_children_category, name='female_children_category'),
    path('cart/<item_id>/increment/', quantity_increment, name='q_incr'),
    path('cart/<item_id>/decrement/', quantity_decrement, name='q_decr'),
    path('cart/<item_id>/delete/', delete_order_item, name='del_item'),
    path('checkout/', checkout, name='checkout'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('add-product/', add_product_view, name='add-product'),
    path('users/', include('Accounts.urls')),
    # re_path(r'^update_item/$', updateItem, name='update_item'),
    path('no_cart/', no_cart, name='no_cart'),
    path('no_checkout', no_checkout, name='no_checkout'),
    # path('ajax/load-cities/', load_cities, name='ajax_load_cities'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="password/password_change_done.html"), name="password_change_done"),

    # path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password/password_change.html'), name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_done.html"), name="password_reset_done"),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name="password_reset_complete"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password/password_reset_form.html', 
        success_url = reverse_lazy('password_reset_complete'),
    ), name="password_reset_confirm"),    

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password/password_reset.html',
        email_template_name='password/password_reset_email.html',
        subject_template_name='password/password_reset_subject.txt',
        success_url = reverse_lazy('password_reset_done'),
    ), name='password_reset'),
    
]




# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)