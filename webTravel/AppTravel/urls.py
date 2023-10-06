
from django.urls import path
from AppTravel.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',user_login,name='user_login'), 
    path('register/',user_register,name='user_register'),
    path('logout/',LogoutView.as_view(template_name='logout.html'),name='user_logout'), 
    path('home/',HomeView.as_view(),name='home'),
    path('travels/',TravelListView.as_view(),name='travels'),
    path('travel-detail/<pk>',TravelDetailView.as_view(),name='travel'),
    path('contact/',contact,name='contact'),
    path('about-us/',aboutUs,name='about'),
    path('orders/',OrdersView.as_view(),name='orders'),
    path('user/',user_edit,name='user'),
    path('buy/<travelid>',buy_travel,name='buy')
]
