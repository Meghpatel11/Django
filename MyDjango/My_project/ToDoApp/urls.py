from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logOut,name='logout'),
    path('user/',views.UserPage,name='user'),
    path('account/',views.accountSettings,name='account'),
    path('register/',views.registerPage,name='register'),
    path('customer/<str:pk>/', views.coustomer, name='customer'),
    
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
]

