from django.shortcuts import render, redirect
# import models from product app, not from core app
from product.models import Product, Category
from .forms import SignupForm

# Create your views here.
def index(request):
    products = Product.objects.filter(is_sold=False)[0:6] # get first 6 products
    categories = Category.objects.all()
    return render(request, 'core/index.html', { 
        'categories': categories,
        'products': products
        })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:     
        form = SignupForm()
    return render(request, 'core/signup.html', {
        'form': form
        })
