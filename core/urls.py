from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('book/', views.book_table, name='booking'),
    path('booking-success/', views.booking_success_view, name='booking_success'),
    path('deals/', views.deals_view, name='deals'),
    path('faqs/', views.faq_view, name='faqs'),
]