from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='index'),
    path('success/', views.success, name='success'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('hx_menu_item/', views.hx_menu_item, name='hx_menu_item'),
    path('update_cart/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('hx_cart_total/', views.hx_cart_total, name='hx_cart_total'),

]
