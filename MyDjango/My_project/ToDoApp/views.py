from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import OrderForm, CreatUserForm,CustomerForm
from .filter import OrderFilter
from .decorators import unauthenticated_user, allowed_users


def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username OR Password is incorrect')
                
    context = {}
    return render(request,'ToDoApp/login.html',context)

def logOut(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
#@allowed_users(allowed_roles=['customer'])

def UserPage(request):
    orders = request.user.customer.order_set.all()
    print('ORDERS',orders)

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context={'orders':orders,
            'total_orders':total_orders,
            'delivered': delivered, 'pending': pending}
    return render(request,'ToDoApp/user.html',context)

@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    context={'form':form}
    return render(request,'ToDoApp/customer_set.html',context)

@unauthenticated_user
def registerPage(request):

	form = CreatUserForm()
	if request.method == 'POST':
		form = CreatUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
                
			messages.success(request, 'Account was created for ' + username)

			return redirect('login')

	context = {'form':form}
	return render(request, 'ToDoApp/register.html', context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = Order.objects.count()
    total_customer = Customer.objects.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers,
                'total_orders':total_orders,
                'delivered': delivered, 'pending': pending
                }

    return render(request, 'ToDoApp/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'ToDoApp/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def coustomer(request,pk):
    coustomer = Customer.objects.get(id=pk)

    orders = coustomer.order_set.all()
    total_orders = orders.count()
    
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders =myFilter.qs
    context = {'customer': coustomer, 'orders':orders,'total_orders':total_orders, 'myFilter':myFilter}
    return render(request, 'ToDoApp/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('status','product'))
    coustomer = Customer.objects.get(id=pk)
    formset = OrderFormSet(instance=coustomer)
    #form = OrderForm(initial={"customer":coustomer})
    if request.method == "POST":
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=coustomer)
        if formset.is_valid():
            formset.save()
            return redirect('/') 

    context = {'formset': formset }
    return render(request,'ToDoApp/order_forms.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/') 

    context = {'form':form}
    return render(request,'ToDoApp/order_forms.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request,'ToDoApp/delete.html', context)

    