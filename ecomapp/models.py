from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# product model

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=5, decimal_places=2)
    available_quantity = models.IntegerField(verbose_name="Available Quantity")
    product_desc = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to="product_img", default="product_img/backimg.jpg")
        
    def __str__(self):
        return self.product_name
    
# User profile Models
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    profileimg = models.ImageField(upload_to="product_img", default="product_img/backimg.jpg")
    

# Reviews MOdel
class Reviews(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField(max_length=255)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.rating
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.cart
    def totalPrice(self):
        return self.quantity*self.product.product_price
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    country = CountryField(blank_label='(Select country)', default='NP')
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2)
    orderDate = models.DateField(auto_now_add=True)
    orderStatus = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItems(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2,default=100.00)
    
    def subtotal(self):
        return self.quantity*self.price
    
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    walletid=models.CharField(max_length=80,default='552555555555')
    ammount = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.BooleanField(default=False)
    paid_date = models.DateField(auto_now_add=True)
    
    