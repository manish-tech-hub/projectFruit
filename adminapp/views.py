from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from .forms import AddProductForm
from ecomapp import models
Product = models.Product
Orderlist = models.Order
OrderItems = models.OrderItems

# Create your views here.
def hello(request):
    return render(request,'adminindex.html')
def mproduct(request):
    query = request.GET.get('query','')
    if query:
        manageproduct = Product.objects.filter(
            product_name__icontains=query
            ) | Product.objects.filter(
            product_price__icontains=query
            ) | Product.objects.filter(
            product_desc__icontains=query
            )
    else:
        manageproduct=Product.objects.all()
    context={
        "query":query,
        "manageproduct":manageproduct
    }
    

    return render(request,'manageproduct.html',context)

# deleting product 
def delete_product(request, product_id):
    proid= get_object_or_404(Product, id=product_id)
    proid.delete()
    return redirect('products')

# adding products
def add_product(request):
    if request.method=='POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('products')
    else:
        form = AddProductForm()
    return render(request,'addproduct.html',{'form':form})

# updating product here
def update(request, product_id):
    product_update = get_object_or_404(Product,id=product_id)
    if request.method =='POST':
        form = AddProductForm(request.POST, request.FILES, instance=product_update)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = AddProductForm(instance=product_update)
    return render(request,'updateproduct.html',{'form':form})

def orderlist(request):
    order = Orderlist.objects.all()
    return render(request,'orderlist.html',{'order':order})

def deleteOrder(request, order_id):
    order = get_object_or_404(Orderlist, id=order_id)
    order.delete()
    return redirect('orderlist')

def orderdetail(request, order_id):
    order = get_object_or_404(Orderlist, id=order_id)
    order_item = OrderItems.objects.filter(order=order)
    total = sum(item.subtotal() for item in order_item)
    if request.method=='POST':
        order.orderStatus=request.POST.get('status')
        order.save()
        return redirect('orderdetail', order_id=order.id)
    return render(request,'orderdetails.html',{'order':order, 
                                               'order_item':order_item,
                                               'total':total})


# for usermanagement
def usermanage(request):
    userobj = User.objects.filter(is_staff=False).values('id','first_name','last_name',
                                                         'username','last_login','date_joined',
                                                         'email')
    return render(request,'user.html',{'user':userobj})

def updateuser(request,user_id):
    userobj = get_object_or_404(User,id=user_id)
    if request.method=='POST':
        first_name = request.POST.get("first_name","").strip()
        Last_name = request.POST.get("last_name","").strip()
        email = request.POST.get("email","").strip()
        password = request.POST.get("password","").strip()
        userobj.first_name = first_name
        userobj.last_name = Last_name
        userobj.email = email
        userobj.username = email
        if password:
            userobj.password = make_password(password)
        userobj.save()
        return redirect('user')
    return render(request,'userupdate.html',{'users':userobj})

def deleteuser(request,user_id):
    userobj = get_object_or_404(User,id = user_id)
    if request.method=='POST':
        userobj.delete()
        return redirect('user')
    
def adminlogin(request):
    if request.method=='POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        adminl = authenticate(request, username=username,password=password)
        if adminl is not None:
            login(request, adminl)
            return redirect('products')
        
    return render(request,'adminlogin.html')

def adminlogout(request):
    logout(request)
    return redirect('adminlogin')










