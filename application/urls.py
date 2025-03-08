from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',index_view,name='index'),
    path('product/<int:product_id>/',product_view,name='product'),
    path('cart/',cart_view,name='cart'),
    path('signup/',signup_view,name='signup'),
    path('signin/',signin_view,name='signin'),
    path('add-to-cart/<str:model_name>/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>/',remove_from_cart,name='remove_from_cart'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('process-payment/', process_payment, name='process_payment'),

]