from django.shortcuts import render,redirect
from core.forms import *
from django.contrib import messages
from core.models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
import random
import string
# 
# Create your views here.
def index(request):
    products=Product.objects.all()
    categories = Category.objects.all()
    return render(request,'core/index.html',{'products':products,'categories': categories})
def add_product(request):
    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request,"Product Added Scuccessfully")
            return redirect('/')
        else:
            print(form.errors)
            messages.info(request,"product is not added,Try Again")
    else:
        form=ProductForm()
    return render(request,'core/add_product.html',{'form':form}) 
def product_desc(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,'core/product_desc.html',{'product':product})
def add_to_cart(request,pk):
    # get that particular product of id=pk
    product=Product.objects.get(pk=pk)
    # create order item
    order_item,created=OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    ) 
    # get queryset of order object of particular user
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item.quantity+=1
            order_item.save()
            messages.info(request,"Added Quantity Item")
            return redirect('product_desc',pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request,"item addes to cart")
            return redirect('product_desc',pk=pk)
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item added to Cart")
        return redirect("product_desc",pk=pk)
def orderlist(request):
    if Order.objects.filter(user=request.user,ordered=False).exists():
        order=Order.objects.get(user=request.user,ordered=False)
        return render(request,'core/orderlist.html',{'order':order})
    return render(request,'core/orderlist.html',{'message':"Your Cart is Empty"})
def add_item(request,pk):
     # get that particular product of id=pk
    product=Product.objects.get(pk=pk)
    # create order item
    order_item,created=OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    ) 
    # get queryset of order object of particular user
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            if order_item.quantity < product.product_available_count:
                order_item.quantity+=1
                order_item.save()
                messages.info(request,"Added Quantity Item")
                return redirect('orderlist')
            else:
                messages.info(request,"Sorry ! product is out of stock")
                return redirect("orderlist")
        else:
            order.items.add(order_item)
            messages.info(request,"item addes to cart")
            return redirect('orderlist')
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item added to Cart")
        return redirect("product_desc",pk=pk)
def remove_item(request,pk):
    item=get_object_or_404(Product,pk=pk)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered=False,
    )
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item=OrderItem.objects.filter(
                product=item,
                user=request.user,
                ordered=False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity-=1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request,"Item quantity was updated")
            return redirect("orderlist")
        else:
            messages.info(request,"This item is not in your cart")
            return redirect("orderlist")
    else:
        messages.info(request,"You Do not have any order")
        return redirect("orderlist")
def get_current_user_address(request):
    customer = Customer.objects.get(user=request.user)
    order = Order.objects.get(user=request.user)
    o=order.ordered_date
    modified_date = o.date() + timedelta(days=7)
    return render(request,'core/delivery.html',{'address':customer.address,'date':modified_date})
def payment(request):
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    digits = ''.join(random.choices(string.digits, k=4))
    random_code = letters + digits
    return render(request,'core/payment.html',{'random_code':random_code})