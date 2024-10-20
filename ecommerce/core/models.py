from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100, blank=False,default="first name")
    lastname = models.CharField(max_length=100, blank=False,default="last name")
    phone_field = models.CharField(max_length=12, blank=False)
    age = models.PositiveIntegerField(blank=False, null=True)
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    gender = models.CharField(max_length=6, choices=gender_choices, blank=False , default='male')
    address = models.CharField(max_length=255, blank=False)
    city = models.CharField(max_length=100, blank=False)
    zip_code = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return self.user.username
# category Model where different Categories will be stored
class Category(models.Model):
    category_name=models.CharField(max_length=200)
    def __str__(self):
        return self.category_name

class Product(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    desc=models.TextField()
    price=models.FloatField(default=0.0)
    product_available_count=models.IntegerField(default=0)
    img=models.ImageField(upload_to='images/')
    img1=models.ImageField(upload_to='images/',default="hello")
    img2=models.ImageField(upload_to='images/',default="hello")
    img3=models.ImageField(upload_to='images/',default="hello")

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart",kwargs={
            "pk":self.pk
        })
    def __str__(self):
        return self.name
class OrderItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    def get_total_item_price(self):
        return self.quantity * self.product.price
    def get_final_price(self):
        return self.get_total_item_price()
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    order_id=models.CharField(max_length=100,unique=True,default=None,blank=True,null=True)
    datetime_ofpayment=models.DateTimeField(auto_now_add=True)
    order_deleivered=models.BooleanField(default=False)
    order_received=models.BooleanField(default=False)

    razorpay_order_id=models.CharField(max_length=500,null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=500,null=True,blank=True)
    razorpay_signature=models.CharField(max_length=500,null=True,blank=True)
    def save(self,*args,**kwargs):
        if self.order_id is None and self.datetime_ofpayment and self.id:
            self.order_id=self.datetime_ofpayment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args,**kwargs)
    def __str__(self):
        return self.user.username
    def get_total_price(self):
        total=0
        for order_item in self.items.all():
            total+=order_item.get_final_price()
        return total
    def get_total_count(self):
        order=Order.objects.get(pk=self.pk)
        return order.items.count()