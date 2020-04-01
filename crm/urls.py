from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('products/', views.products, name='product-view'),
    path('customer/<str:pk>/', views.customers, name='customer-view'),

    path('customer-order/<str:pk>/', views.PlaceOrder, name='place-order'),
    path('update-order/<str:pk>/', views.updateOrder, name="update-order"),
    path('delete-order/<str:pk>/', views.deleteOrder, name="delete-order"),

    # REGISTRATION FOR APPLICATION #
    path('applications/', login_required(views.ApplicationList.as_view(), login_url='login'), name='application-list'),
    path('create/', login_required(views.ApplicationCreate.as_view(), login_url='login'), name='create-application'),
    path('create/<int:pk>/', login_required(views.ApplicationUpdate.as_view(), login_url='login'), name='update-application'),
    path('delete/<int:pk>', login_required(views.ApplicantDelete.as_view(), login_url='login'), name='delete-application'),


]