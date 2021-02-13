"""ShopWithAyo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from product_category import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.basePage, name='base'),
    path('', views.homePage, name='home'),


    path('jeans/', views.jeansPage, name='jeans'),
    path('shirts/', views.shirtsPage, name='shirts'),
    path('coats/', views.coatsPage, name='coats'),
    path('sweats/', views.sweatsPage, name='sweats'),


    path('jeans/details/<int:id>/', views.product_details, name='jeans'),
    path('shirts/details/<int:id>/', views.product_details, name='shirts'),
    path('coats/details/<int:id>/', views.product_details, name='coats'),
    path('sweats/details/<int:id>/', views.product_details, name='details'),


    path('cart/', views.cartPage, name='cart'),
    path('checkout/', views.checkoutPage, name='checkout'),

    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)