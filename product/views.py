from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q # Q is a shortcut for OR queries
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from .forms import NewProductForm, EditProductForm
# Create your views here.

def products(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0) # 0 is the default value if category_id is not found
    categories = Category.objects.all()
    products = Product.objects.filter(is_sold=False)
    
    
    if category_id:
        products = products.filter(category_id=category_id) # filter by category_id = category_id from the url


    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query)) # Q is a shortcut for OR queries
        # import Q from django.db.models


    
    return render(request, 'product/products.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })



def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'product/detail.html', {
        'product': product,
        'related_products': related_products
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            
            return redirect('product:detail', pk=product.id)
        else: 
            form = NewProductForm()

    form = NewProductForm()
    
    return render(request, 'product/form.html', {
        'form': form,
        'title': 'New Product'
    })

@login_required
def edit(request, pk):
    print('line 63',pk)
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    # get_object_or_404 is a shortcut that will return a 404 error if the object is not found
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        print("form",form.is_valid())
        if form.is_valid():
            product = form.save()
            
            product.save()


            return redirect('product:detail', pk=product.id)
    else: 
            form = EditProductForm(instance=product)

    
    
    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Update Product'
    })

@login_required
def delete(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    product.delete()
    return redirect('dashboard:index')