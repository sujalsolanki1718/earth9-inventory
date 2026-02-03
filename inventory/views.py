import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product, Bill
from .forms import ProductForm, BillForm
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import F, Sum
from .models import Product



def logout_view(request):
    logout(request)
    return redirect('login')  

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

@login_required(login_url='login')


def dashboard(request):
    products = Product.objects.filter(user=request.user)

    product_data = list(products.values('name', 'qty'))

    total_products = products.count()

    
    stock_value = products.aggregate(
        total=Sum(F('sell_price') * F('qty'))
    )['total'] or 0

    
    low_stock = products.filter(qty__lte=F('min_stock')).count()

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.user = request.user
            prod.save()
            return redirect('dashboard')
    else:
        form = ProductForm()

    return render(request, 'dashboard.html', {
        'products': products,
        'form': form,
        'product_data': product_data,
        'total_products': total_products,   
        'stock_value': stock_value,         
        'low_stock': low_stock,        
    })


@login_required
def billing(request):
    bills = Bill.objects.filter(user=request.user)

    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()
            return redirect('billing')
    else:
        form = BillForm()

    return render(request, 'billing.html', {'bills': bills, 'form': form})


@login_required
def export_csv(request):
    products = Product.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Code', 'Sell', 'Purchase', 'Qty'])

    for p in products:
        writer.writerow([p.name, p.code, p.sell_price, p.purchase_price, p.qty])

    return response


@login_required
def edit_product(request, id):
    product = Product.objects.get(id=id, user=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form})


@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id, user=request.user)
    product.delete()
    return redirect('dashboard')
