from django.urls import path,include
from .views import hello,mproduct,delete_product,add_product,update,orderlist,deleteOrder,orderdetail,usermanage,updateuser
from .views import deleteuser,adminlogin,adminlogout
urlpatterns = [
    path('',adminlogin, name='adminlogin'),
    path('products/',mproduct, name='products'),
    path('delete/<int:product_id>/',delete_product, name='delete'),
    path('addproduct/',add_product, name='addproduct'),
    path('update/<int:product_id>/',update, name='update'),
    path('orderlist/',orderlist, name='orderlist'),
    path('orderdelete/<int:order_id>/',deleteOrder, name='orderdelete'),
    path('orderdetail/<int:order_id>/',orderdetail, name='orderdetail',),
    path('user/',usermanage, name='user'),
    path('userupdate/<int:user_id>/',updateuser,name='userupdate'),
    path('userdelete/<int:user_id>/',deleteuser,name="userdelete"),
    path('logout/',adminlogout,name='adminlogout')
    
]
