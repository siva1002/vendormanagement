from django.contrib import admin
from django.urls import path
from .views import(vendorapp)
from .apis import (PurchaseAPI,VendorsGetUpdateAPI,VendorsCreate,PurchaseUpdateAPI,VendorPerformance,LoginView)

urlpatterns = [
    path('', vendorapp,name="home"),
    path('login/',LoginView.as_view(),name="login"),
    path('vendors/',VendorsCreate.as_view(),name='vendors'),
    path('vendors/<int:pk>/',VendorsGetUpdateAPI.as_view(),name='vendorsgetupdte'),
    path("vendors/<int:pk>/performance",VendorPerformance.as_view()),
    path('purchase_order/',PurchaseAPI.as_view(),name='deliveryrate'),
    path('purchase_order/<int:pk>',PurchaseUpdateAPI.as_view(),name='deliveryrate'),
    
]
