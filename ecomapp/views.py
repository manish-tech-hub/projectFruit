from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Reviews, Cart,CartItems,Order,UserProfile,OrderItems,Payment
from .forms import UserRegistration
from  django.contrib.auth import authenticate,login,logout
from .forms import LoginForm,OrderForm




# Create your views here.
def home(request):
    Products = Product.objects.all()
    return render(request,'index.html',{'Products':Products})

def search(request):
    query = request.GET.get('query','')
    product = Product.objects.filter(product_name__icontains=query) if query else []
    return render(request,'searchitems.html',{'product':product,'query':query})

@login_required
def productdetail(request, product_id):
    product = Product.objects.get(id=product_id)
    reviews = Reviews.objects.filter(product_name=product).order_by("created_at")
    related_products = Product.objects.exclude(id=product.id).order_by('?')[:4]

    if request.method =='POST':
        rating = request.POST.get('rating')
        text = request.POST.get('text')

        if rating and text:
            Reviews.objects.create(
                product_name=product,
                user = request.user,
                rating = int(rating),
                text = text
            )
        return redirect('productdetail',product_id = product.id)
    
    return render(request, 'productdetail.html', {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
    })
def addToCart(request,product_id):
    product = Product.objects.get(id=product_id)
    user = request.user if request.user.is_authenticated else None
    cart, created = Cart.objects.get_or_create(user=user)
    detailquantity = int(request.POST.get('qty'))

    cartItem, cartitem_created = CartItems.objects.get_or_create(cart=cart, product=product)
    totalqty = detailquantity if cartitem_created else cartItem.quantity

    if totalqty > product.available_quantity:
        messages.warning(request, f"Only {product.available_quantity} item's available in stock.")
        return redirect('productdetail', product_id=product_id)
    cartItem.quantity = totalqty
    cartItem.save()
    messages.success(request, f"{detailquantity} item(s) added to your cart.")
    return redirect('cart')

def view_cart(request):
    user = request.user if request.user.is_authenticated else None
    cart = Cart.objects.filter(user=user).first()
    cart_items = cart.items.all() if cart else []
    total = sum(item.totalPrice() for item in cart_items)
    totalQuant = sum(items.quantity for items in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'totalQuant':totalQuant})

def increaseQuantity(request, item_id):
    if request.method=='POST':
        item = CartItems.objects.get(id=item_id)
        availableqty = item.product.available_quantity
        if availableqty > item.quantity:
            item.quantity +=1
            item.save()
        else:
            messages.warning(request,'you teached available quantity limit')
        return redirect('cart')
    
def decreaseQuantity(request,item_id):
    if request.method=='POST':
        item = CartItems.objects.get(id=item_id)
        if item.quantity > 1:
            item.quantity-=1
        item.save()
        return redirect('cart')
    
def deleteItem(request,item_id):
    if request.method=='POST':
        item = CartItems.objects.get(id=item_id)
        item.delete()
        return redirect('cart')
def singin(request):
    if request.method =='POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember_me')
            user = authenticate(request, username=username, password = password)
            if user is not None:
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(10000)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request,'singin.html',{'form':form})
def singup(request):
    if request.method =='POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('singin')
    else:
       form = UserRegistration()
    return render(request,'singup.html',{'form':form})
def checkout(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    cartItems = cart.items.all() if cart else []
    total = sum(item.totalPrice() for item in cartItems)
    totalQuant = sum(item.quantity for item in cartItems)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Try to get an unpaid order or create one with required fields set
            order, created = Order.objects.get_or_create(
                user=user,
                is_paid=False,
                defaults={
                    'cart': cart,
                    'totalPrice': total,
                    # You can set other mandatory fields here if any
                }
            )
            
            if not created:
                # Update order fields for existing order
                order.cart = cart
                order.totalPrice = total
            
            # Update order fields from form
            order.firstName = form.cleaned_data['firstName']
            order.lastName = form.cleaned_data['lastName']
            order.country = form.cleaned_data['country']
            order.city = form.cleaned_data['city']
            order.state = form.cleaned_data['state']
            order.zipCode = form.cleaned_data['zipCode']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']

            order.save()
            
            # Store products in OrderItems (only if new order or no items yet)
            if created or not OrderItems.objects.filter(order=order).exists():
                for item in cartItems:
                    OrderItems.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.product_price,
                    )
                    # Update product available quantity
                    item.product.available_quantity -= item.quantity
                    item.product.save()
                    # Remove item from cart
                    item.delete()

            return redirect('payment')
    else:
        # Autofill address from last order if exists
        last_order = Order.objects.filter(user=user).order_by('-id').first()
        if last_order:
            form = OrderForm(initial={
                'firstName': last_order.firstName,
                'lastName': last_order.lastName,
                'country': last_order.country,
                'city': last_order.city,
                'state': last_order.state,
                'zipCode': last_order.zipCode,
                'phone': last_order.phone,
                'email': last_order.email,
            })
        else:
            form = OrderForm()

    return render(request, 'checkout.html', {
        'form': form,
        'cart': cartItems,
        'total': total,
        'totalQuan': totalQuant
    })


@login_required
def userProfile(request):
    userdetail = request.user
    userinfo = UserProfile.objects.get(user = userdetail)
    user_address = Order.objects.filter(user=userdetail).order_by('-id').first()
    recent_orders = Order.objects.filter(user=userdetail).order_by('-id')[:5]
    if request.method =='POST':
        full_name = request.POST.get("full_name"," ").strip()
        number = request.POST.get("number")
        email = request.POST.get("email")
        name = full_name.split(maxsplit=1)
        userdetail.first_name=name[0]
        userdetail.last_name=name[1] if len(name)>1 else ""
        userdetail.email = email
        userdetail.save()
        userinfo.mobile = number
        userinfo.save()
        return redirect('profile')
    return render(request, 'profile.html',{
        'detail':userdetail,
        'userinfo':userinfo,
        'user_address':user_address,
        'recent_order':recent_orders
        })
def userlogout(request):
    logout(request)
    return redirect("/")
@login_required
def profileupdate(request):
    userinfo = UserProfile.objects.get(user = request.user)
    if request.method=='POST' and request.FILES.get('profile_pic'):
        profile_pic = request.FILES.get('profile_pic')
        userinfo.profileimg = profile_pic
        userinfo.save()
        return redirect('profile')
    return render(request, "profileupdate.html",{'userinfo':userinfo})

@login_required
def for_payment(request):
    user = request.user
    order = Order.objects.filter(user=user,is_paid=False).order_by('-id').first()
    if order:
        total = order.totalPrice
    else:
        total=0
    if request.method=='POST':
        walletid = request.POST.get('gateway_id')
        ammount =int( request.POST.get('ammount'))

        if order and ammount == total:
            payment = Payment.objects.create(
            user=user, walletid=walletid,ammount=ammount, status=True)

            order.is_paid=True
            order.save()

            return redirect('index')
        else:
            messages.error(request,'ammount must be same as total aamount')
    return render(request,'payment.html',{'total':total})
