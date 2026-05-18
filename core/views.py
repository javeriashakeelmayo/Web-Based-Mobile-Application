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
        # ... aapka purana booking creation ka code yahan rahega ...
        name_val = request.POST.get('name')
        phone_val = request.POST.get('phone')
        date_val = request.POST.get('date')
        guests_val = request.POST.get('guests')
        time_val = request.POST.get('time')
        
        Booking.objects.create(
            name=name_val, phone=phone_val, date=date_val, 
            guests=guests_val, time_slot=time_val
        )
        return render(request, 'core/booking_success.html')


    from datetime import date
    today_str = date.today().strftime('%Y-%m-%d')
    

    full_slots_query = Booking.objects.filter(date=date.today())\
                                      .values('time_slot')\
                                      .annotate(total=Count('id'))\
                                      .filter(total__gte=5)
    

    full_slots = [slot['time_slot'] for slot in full_slots_query]

    return render(request, 'core/booking.html', {'full_slots': full_slots})

def booking_success_view(request):
    return render(request, 'core/booking_success.html')

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