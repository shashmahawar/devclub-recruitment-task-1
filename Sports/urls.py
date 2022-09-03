from django.urls import path
from . import views

urlpatterns = [
    path('', views.sports, name='sports'),
    path('filter/<str:pk>/', views.sports_filter, name='sports_filter'),
    path('confirmed', views.confirmed, name='confirmed'),
    path('<str:sport>/', views.sports_detail, name='sports_detail'),
    path('<str:sport>/book/', views.book, name='book'),
    # API URLs
    path('api/getSlots/', views.getSlots, name='getSlots'),
    path('api/getAvailability/', views.getAvailability, name='getAvailability'),
]
