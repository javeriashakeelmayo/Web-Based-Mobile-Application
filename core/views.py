from django.shortcuts import render, redirect
from .models import Category, MenuItem, Booking, Lead
from django.contrib import messages

def home(request):
    specials = MenuItem.objects.all()[:3] 
    return render(request, 'core/home.html', {'specials': specials})

def menu(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    
    if category_id:
        items = MenuItem.objects.filter(category_id=category_id)
    else:
        items = MenuItem.objects.all()
        
    return render(request, 'core/menu.html', {
        'categories': categories,
        'items': items
    })

def book_table(request):
    if request.method == "POST":
        # Form se data uthana (HTML input names ke mutabiq)
        name_val = request.POST.get('name')
        phone_val = request.POST.get('phone')
        date_val = request.POST.get('date')
        guests_val = request.POST.get('guests')
        time_val = request.POST.get('time')

        booking = Booking.objects.create(
            name=name_val,
            phone=phone_val,
            date=date_val,
            guests=guests_val,
            time_slot=time_val
        )
        
        return render(request, 'core/booking_success.html', {'booking': booking})
    
    return render(request, 'core/booking.html')

def booking_success_view(request):
    return render(request, 'core/booking_success.html')

def deals_view(request):
    return render(request, 'core/deals.html')

def faq_view(request):
    return render(request, 'core/faqs.html')