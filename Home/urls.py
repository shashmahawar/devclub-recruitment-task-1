from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signup/verify/', views.signup_otp, name='signup_otp'),
    path('forgot/', views.reset, name='reset'),
    path('forgot/verify/', views.reset_otp, name='reset_otp'),
    path('forgot/reset/<str:username>/', views.reset_password, name='reset_password'),
    path('bookings/', views.bookings, name='bookings'),
]
