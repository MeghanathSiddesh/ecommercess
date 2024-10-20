from django.urls import path
from core.views import *

urlpatterns = [
    path('',index,name='index'),
    path('add_product',add_product,name="add_product"),
    path('product_desc/<pk>',product_desc,name="product_desc"),
    path('add_to_cart/<pk>',add_to_cart,name="add_to_cart"),
    path('orderlist',orderlist,name="orderlist"),
    path('add_item/<int:pk>',add_item,name="add_item"),
    path('remove_item/<int:pk>',remove_item,name="remove_item"),
    path('get_current_user_address',get_current_user_address,name="get_current_user_address"),
    path('payment',payment,name="payment"),
]