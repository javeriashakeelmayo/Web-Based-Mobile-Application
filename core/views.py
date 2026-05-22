from django.shortcuts import render, redirect
from .models import Category, MenuItem, Booking, Lead
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from .models import MenuItem
from django.db.models import Count

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
        name_val = request.POST.get('name')
        phone_val = request.POST.get('phone')
        date_val = request.POST.get('date')
        guests_val = request.POST.get('guests')
        time_val = request.POST.get('time')
        
        # 1. Booking object ko create kar ke variable mein store kiya
        new_booking = Booking.objects.create(
            name=name_val, phone=phone_val, date=date_val, 
            guests=guests_val, time_slot=time_val
        )
        
        # 2. Template ko render karte waqt naye booking object ko context mein pass kiya
        return render(request, 'core/booking_success.html', {'booking': new_booking})

    # --- GET Request Logic (Dynamic Date Handling) ---
    from datetime import date
    
    target_date_str = request.GET.get('date')
    if target_date_str:
        try:
            from datetime import datetime
            target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = date.today()
    else:
        target_date = date.today()

    full_slots_query = Booking.objects.filter(date=target_date)\
                                      .values('time_slot')\
                                      .annotate(total=Count('id'))\
                                      .filter(total__gte=5) 
    
    full_slots = [slot['time_slot'] for slot in full_slots_query]

    return render(request, 'core/booking.html', {'full_slots': full_slots})

def booking_success_view(request):
    latest_booking = Booking.objects.last()
    return render(request, 'core/booking_success.html', {'booking': latest_booking})

def deals_view(request):
    return render(request, 'core/deals.html')

def faq_view(request):
    return render(request, 'core/faqs.html')



def update_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = str(data.get('item_id'))
        action = data.get('action', 'add') # 'add' ya 'remove' ya 'clear'
        
        # Session se purana cart nikalwein, agar nahi hai to khali {} banayein
        cart = request.session.get('cart', {})
        
        try:
            item = MenuItem.objects.get(id=item_id)
        except MenuItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item nahi mila'})
            
        if action == 'add':
            if item_id in cart:
                cart[item_id]['quantity'] += 1
            else:
                cart[item_id] = {
                    'name': item.name,
                    'price': float(item.price),
                    'quantity': 1
                }
        elif action == 'remove':
            if item_id in cart:
                cart[item_id]['quantity'] -= 1
                if cart[item_id]['quantity'] <= 0:
                    del cart[item_id]
                    
        # Django session ko save karein
        request.session['cart'] = cart
        request.session.modified = True
        
        # Naye totals nikalwein
        total_items = sum(info['quantity'] for info in cart.values())
        total_price = sum(info['price'] * info['quantity'] for info in cart.values())
        
        return JsonResponse({
            'success': True,
            'total_items': total_items,
            'total_price': f"{total_price:.2f}"
        })


def get_cart_status(request):
    cart = request.session.get('cart', {})
    total_items = sum(info['quantity'] for info in cart.values())
    total_price = sum(info['price'] * info['quantity'] for info in cart.values())
    return JsonResponse({
        'total_items': total_items,
        'total_price': f"{total_price:.2f}"
    })
# Views ke end par yeh naya view function add karein
def checkout(request):
    # Abhi ke liye hum sirf checkout.html template render karwa rahe hain
    return render(request, 'core/checkout.html')