from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, MenuItem, Reservation
from .forms import ReservationForm, ContactForm

#after delete me
from .forms import VideoForm
from .models import Video

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = VideoForm()

    videos = Video.objects.all().order_by('-uploaded_at')
    return render(request, 'home/video.html', {'form': form, 'videos': videos})





def index(request):
    featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)[:6]
    categories = Category.objects.all()[:4]
    
    context = {
        'featured_items': featured_items,
        'categories': categories,
    }
    return render(request, 'home/index.html', context)

def menu(request):
    categories = Category.objects.all()
    
    # Handle category filtering
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        menu_items = MenuItem.objects.filter(category=category, is_available=True)
    else:
        menu_items = MenuItem.objects.filter(is_available=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        menu_items = menu_items.filter(name__icontains=search_query)
    
    context = {
        'categories': categories,
        'menu_items': menu_items,
        'selected_category': category_slug,
        'search_query': search_query if search_query else '',
    }
    return render(request, 'home/menu.html', context)

def menu_item_detail(request, slug):
    menu_item = get_object_or_404(MenuItem, slug=slug, is_available=True)
    related_items = MenuItem.objects.filter(category=menu_item.category).exclude(id=menu_item.id)[:4]
    
    context = {
        'menu_item': menu_item,
        'related_items': related_items,
    }
    return render(request, 'home/menu_item_detail.html', context)

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'home/contact.html', context)

def reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your reservation has been submitted successfully!')
            return redirect('home:reservation')
    else:
        form = ReservationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'home/reservation.html', context)