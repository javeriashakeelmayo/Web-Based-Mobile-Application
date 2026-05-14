from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('book/', views.book_table, name='booking'),
    path('booking-success/', views.booking_success_view, name='booking_success'),
    path('deals/', views.deals_view, name='deals'),
    path('faqs/', views.faq_view, name='faqs'),
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json')),
        path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript')),
]