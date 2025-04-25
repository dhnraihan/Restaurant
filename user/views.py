from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from django.utils import timezone
import os
import random
import string
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Profile, Order, OrderItem, Invoice
from .forms import ProfileForm, OrderForm
from home.models import MenuItem

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('user:dashboard')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'user/register.html', context)

@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'user/dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    
    context = {
        'form': form,
    }
    return render(request, 'user/profile.html', context)

@login_required
def cart(request):
    # Get cart from session or create empty cart
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    # Process cart items
    for item_id, quantity in cart.items():
        try:
            menu_item = MenuItem.objects.get(id=item_id)
            subtotal = menu_item.price * quantity
            total += subtotal
            cart_items.append({
                'id': menu_item.id,
                'name': menu_item.name,
                'price': menu_item.price,
                'quantity': quantity,
                'subtotal': subtotal,
                'image': menu_item.image.url,
            })
        except MenuItem.DoesNotExist:
            pass
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'user/cart.html', context)

@login_required
def add_to_cart(request, item_id):
    # Get cart from session or create empty cart
    cart = request.session.get('cart', {})
    
    # Add item to cart
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, 'Item added to cart!')
    
    # Redirect back to the referring page
    return redirect(request.META.get('HTTP_REFERER', 'home:menu'))

@login_required
def remove_from_cart(request, item_id):
    # Get cart from session
    cart = request.session.get('cart', {})
    
    # Remove item from cart
    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart
        messages.success(request, 'Item removed from cart!')
    
    return redirect('user:cart')

@login_required
def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                item_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    if quantity > 0:
                        cart[item_id] = quantity
                    else:
                        del cart[item_id]
                except ValueError:
                    pass
        
        request.session['cart'] = cart
        messages.success(request, 'Cart updated successfully!')
    
    return redirect('user:cart')

@login_required
def checkout(request):
    # Get cart from session
    cart = request.session.get('cart', {})
    
    # Check if cart is empty
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('user:cart')
    
    # Get cart items
    cart_items = []
    total = 0
    
    for item_id, quantity in cart.items():
        try:
            menu_item = MenuItem.objects.get(id=item_id)
            subtotal = menu_item.price * quantity
            total += subtotal
            cart_items.append({
                'id': menu_item.id,
                'name': menu_item.name,
                'price': menu_item.price,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except MenuItem.DoesNotExist:
            pass
    
    # Process checkout
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create order
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total
            order.save()
            
            # Create order items
            for item_id, quantity in cart.items():
                try:
                    menu_item = MenuItem.objects.get(id=item_id)
                    OrderItem.objects.create(
                        order=order,
                        menu_item=menu_item,
                        quantity=quantity,
                        price=menu_item.price
                    )
                except MenuItem.DoesNotExist:
                    pass
            
            # Generate invoice
            invoice_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            invoice = Invoice.objects.create(
                order=order,
                invoice_number=invoice_number
            )
            
            # Generate PDF invoice
            generate_invoice_pdf(invoice)
            
            # Clear cart
            request.session['cart'] = {}
            
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('user:order_confirmation', order_id=order.id)
    else:
        # Pre-fill form with user profile data
        initial_data = {}
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial_data = {
                'full_name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
                'phone': profile.phone,
                'address': profile.address,
            }
        form = OrderForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'user/checkout.html', context)

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'user/order_confirmation.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'user/order_detail.html', context)

@login_required
def download_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id, order__user=request.user)
    
    # Check if PDF exists, otherwise generate it
    if not invoice.pdf_file:
        generate_invoice_pdf(invoice)
        invoice.refresh_from_db()
    
    # Serve the PDF file
    file_path = os.path.join(settings.MEDIA_ROOT, invoice.pdf_file.name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    
    # If file doesn't exist, generate on-the-fly
    return generate_invoice_pdf_response(invoice)

def generate_invoice_pdf(invoice):
    # Create a BytesIO object
    buffer = io.BytesIO()
    
    # Create the PDF object using the BytesIO object as its "file"
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Draw the invoice
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Invoice")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 720, f"Invoice #: {invoice.invoice_number}")
    p.drawString(50, 700, f"Date: {invoice.invoice_date.strftime('%d/%m/%Y')}")
    p.drawString(50, 680, f"Customer: {invoice.order.full_name}")
    p.drawString(50, 660, f"Email: {invoice.order.email}")
    
    # Draw table header
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 620, "Item")
    p.drawString(300, 620, "Quantity")
    p.drawString(370, 620, "Price")
    p.drawString(450, 620, "Subtotal")
    
    # Draw a line
    p.line(50, 610, 550, 610)
    
    # Draw table content
    y = 590
    p.setFont("Helvetica", 10)
    
    for item in invoice.order.items.all():
        p.drawString(50, y, item.menu_item.name)
        p.drawString(300, y, str(item.quantity))
        p.drawString(370, y, f"${item.price}")
        p.drawString(450, y, f"${item.subtotal}")
        y -= 20
    
    # Draw a line
    p.line(50, y - 10, 550, y - 10)
    
    # Draw total
    p.setFont("Helvetica-Bold", 12)
    p.drawString(370, y - 30, "Total:")
    p.drawString(450, y - 30, f"${invoice.order.total_amount}")
    
    # Draw footer
    p.setFont("Helvetica", 10)
    p.drawString(50, 50, "Thank you for your order!")
    
    # Close the PDF object
    p.showPage()
    p.save()
    
    # Get the value of the BytesIO buffer and save it to the invoice
    buffer.seek(0)
    
    # Save PDF to media folder
    file_path = f"invoices/{invoice.invoice_number}.pdf"
    file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
    
    # Write PDF to file
    with open(file_full_path, 'wb') as f:
        f.write(buffer.read())
    
    # Update invoice object
    invoice.pdf_file = file_path
    invoice.save()

def generate_invoice_pdf_response(invoice):
    # Create a BytesIO object
    buffer = io.BytesIO()
    
    # Create the PDF object using the BytesIO object as its "file"
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Draw the invoice (same as above)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Invoice")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 720, f"Invoice #: {invoice.invoice_number}")
    p.drawString(50, 700, f"Date: {invoice.invoice_date.strftime('%d/%m/%Y')}")
    p.drawString(50, 680, f"Customer: {invoice.order.full_name}")
    p.drawString(50, 660, f"Email: {invoice.order.email}")
    
    # Draw table header
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 620, "Item")
    p.drawString(300, 620, "Quantity")
    p.drawString(370, 620, "Price")
    p.drawString(450, 620, "Subtotal")
    
    # Draw a line
    p.line(50, 610, 550, 610)
    
    # Draw table content
    y = 590
    p.setFont("Helvetica", 10)
    
    for item in invoice.order.items.all():
        p.drawString(50, y, item.menu_item.name)
        p.drawString(300, y, str(item.quantity))
        p.drawString(370, y, f"${item.price}")
        p.drawString(450, y, f"${item.subtotal}")
        y -= 20
    
    # Draw a line
    p.line(50, y - 10, 550, y - 10)
    
    # Draw total
    p.setFont("Helvetica-Bold", 12)
    p.drawString(370, y - 30, "Total:")
    p.drawString(450, y - 30, f"${invoice.order.total_amount}")
    
    # Draw footer
    p.setFont("Helvetica", 10)
    p.drawString(50, 50, "Thank you for your order!")
    
    # Close the PDF object
    p.showPage()
    p.save()
    
    # Get the value of the BytesIO buffer
    buffer.seek(0)
    
    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{invoice.invoice_number}.pdf"'
    
    return response