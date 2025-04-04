from itertools import product
from lib2to3.fixes.fix_input import context
from venv import create
from .models import  *
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from app.models import Product
from django.core.paginator import Paginator

from django.template.loader import render_to_string
#Create your views here.

def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = 'hidden' #khi người dùng đã đăng nhập thì ẩn thông tin đăng nhạp
        user_login = 'show'
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = 'show' 
        user_login = 'hidden'
    id = request.GET.get('id', '')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub = False) # danh muc cha
    context={'products':products,'categories':categories,'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login, 'user_login':user_login }
    return render(request,'app/detail.html',context)

def category(request):
    categories = Category.objects.filter(is_sub = False) # danh muc cha
    active_category = request.GET.get('category','')
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = 'hidden' #khi người dùng đã đăng nhập thì ẩn thông tin đăng nhạp
        user_login = 'show'
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = 'show' #khi người dùng đã đăng nhập thì ẩn thông tin đăng nhạp
        user_login = 'hidden'
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context={'categories':categories, 'products':products, 'active_category':active_category,'user_not_login':user_not_login, 'user_login':user_login,'products' :products,'cartItems':cartItems }
    return render(request, 'app/category.html', context)
def search(request):
    categories = Category.objects.filter(is_sub = False) # danh muc cha
    active_category = request.GET.get('category','')
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__icontains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = 'hidden' #khi người dùng đã đăng nhập thì ẩn thông tin đăng nhạp
        user_login = 'show'
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = 'show' #khi người dùng đã đăng nhập thì ẩn thông tin đăng nhạp
        user_login = 'hidden'
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    products = Product.objects.all()
    return render(request, 'app/search.html', {"searched":searched, "keys":keys,'products' :products,'cartItems':cartItems,'user_not_login':user_not_login, 'user_login':user_login,'categories':categories, })

def register(request):
    form = CreateUserForm()    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context={'form':form}
    return render(request, 'app/register.html', context)


def loginPage(request):
    # Kiểm tra nếu người dùng đã đăng nhập, chuyển hướng về trang chủ
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'UserName or Password not correct!')

    context = {}
    return render(request, 'app/login.html', context)
def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = 'hidden'  # Ẩn thông tin đăng nhập khi người dùng đã đăng nhập
        user_login = 'show'
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = 'show'
        user_login = 'hidden'

    categories = Category.objects.filter(is_sub=False)  # Danh mục cha
    products = Product.objects.all()

    # Thêm phân trang
    paginator = Paginator(products, 12)  # Hiển thị tối đa 12 sản phẩm mỗi trang
    page_number = request.GET.get('page')  # Lấy số trang hiện tại từ URL
    page_obj = paginator.get_page(page_number)  # Lấy các sản phẩm của trang hiện tại

    context = {
        'categories': categories,
        'page_obj': page_obj,  # Thay vì truyền 'products', bạn truyền 'page_obj'
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login,
    }
    return render(request, 'app/home.html', context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = 'hidden' #khi người dùng đã đăng nhập thì ẩn thông tin đăng nhạp
        user_login = 'show'
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = 'show' 
        user_login = 'hidden'
    categories = Category.objects.filter(is_sub = False) # danh muc cha
    context={'categories':categories,'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login, 'user_login':user_login }
    return render(request,'app/cart.html',context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        # Lấy hoặc tạo mới một đơn hàng chưa hoàn tất
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = 'hidden'
        user_login = 'show'

        if request.method == 'POST':
            # Lấy thông tin từ form
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')            
            mobile = request.POST.get('mobile')

            # Lưu thông tin địa chỉ vào cơ sở dữ liệu
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=address,
                city=city,
                state=state,
                mobile=mobile
            )
            
            # Đánh dấu đơn hàng là hoàn tất
            order.complete = True
            order.save()

            # Xóa các sản phẩm trong giỏ hàng
            order.orderitem_set.all().delete()

            # Chuyển hướng đến trang xác nhận đặt hàng
            return redirect('order_success')

    else:
        # Xử lý cho người dùng chưa đăng nhập
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = 'show'
        user_login = 'hidden'

    # Lấy danh mục sản phẩm (nếu cần hiển thị trên giao diện)
    categories = Category.objects.filter(is_sub=False)
    context = {
        'categories': categories, 
        'items': items, 
        'order': order, 
        'cartItems': cartItems, 
        'user_not_login': user_not_login, 
        'user_login': user_login
    }
    return render(request, 'app/checkout.html', context)


def order_success(request):
    if request.user.is_authenticated:
        customer = request.user
        user_not_login = 'hidden'
        user_login = 'show'
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        user_not_login = 'show'
        user_login = 'hidden'
        items=[]
        order={'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    # Add any additional context if needed
    context = {'items':items,'order':order,'cartItems':cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login
    }    
    return render(request, 'app/order_success.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
    if action =='add':
        orderItem.quantity +=1
    elif action =='remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse('added',safe=False)