from django.urls import path

from . import views

app_name = 'product'

urlpatterns = [
    path('', views.products, name='products'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete', views.delete, name='delete'),
    path('<int:pk>/edit', views.edit, name='edit'),
    path('<int:pk>/delete_photo/', views.delete_photo, name='delete_photo'),

    # path to add_photo
    path('<int:pk>/add_photo', views.add_photo, name='add_photo'),

]