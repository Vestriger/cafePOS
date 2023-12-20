import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from .models import Category, Product, Worker, Sells, Shifts


def all_categories(request):
    categories = Category.objects.all()
    return render(request, '../templates/show_categories.html', {'categories': categories})


def product_by_category(request, category_slug):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
        return render(request, '../templates/products_by_category.html', {
            'category': category,
            'products': products,
            'slug': category_slug
        })


def delete_category(request, id):
    if id:
        Category.objects.filter(id=id).delete()
    categories = Category.objects.all()
    return render(request, '../templates/show_categories.html', {'categories': categories})


def delete_product(request, slug, id):
    if id:
        category = get_object_or_404(Category, slug=slug)
        Product.objects.filter(id=id, category=category).delete()

    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
        return render(request, '../templates/products_by_category.html', {
            'category': category,
            'products': products,
            'slug': slug
        })


def report(request):
    unique_dates = Sells.objects.values('time_of_sell').distinct()

    summary_data = []

    for date_obj in unique_dates:
        date = date_obj['time_of_sell']

        cash_data = (
            Sells.objects
            .filter(time_of_sell=date, payment_type='cash')
            .values('product', 'worker')
            .annotate(total_value=Sum('value_of_product'))
        )

        card_data = (
            Sells.objects
            .filter(time_of_sell=date, payment_type='card')
            .values('product', 'worker')
            .annotate(total_value=Sum('value_of_product'))
        )

        summary_data.append({
            'date': date,
            'cash': list(cash_data),
            'card': list(card_data),
        })

    context = {'summary_data': summary_data}
    return render(request, '../templates/report.html', context)


def warehouse(request):
    products = Product.objects.all()
    return render(request, '../templates/warehouse.html', {'products': products})


def update_warehouse(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        value = request.POST.get('new_value')

        product = get_object_or_404(Product, id=int(product_id))
        product.value_on_warehouse = int(value)
        product.save()

        return HttpResponse(status=200)
    return HttpResponse(status=400)


def login_worker(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        print(password)
        worker = authenticate(request, password=password)
        if worker is not None:
            login(request, worker)
            return render(request, '../templates/login_worker.html', {'error': 'uu'})
        else:
            return render(request, '../templates/login_worker.html', {'error': 'Неверный пароль'})

    return render(request, '../templates/login_worker.html')


def update_order(request):
    if request.method == 'POST':
        order = json.loads(request.POST.get('order', '{}'))
        products = {}
        total = 0
        products_for_id = Product.objects.all()
        product_ids = [product.id for product in products_for_id]

        for product_id in order:
            if product_id != 'worker_id' and product_id != 'order_number' and int(product_id) in product_ids:
                product = get_object_or_404(Product, id=int(product_id))
                products[product.name] = {'value': order[product_id], 'price': int(product.price), 'id': product_id}
                total += order[product_id] * int(product.price)

        order_html = render_to_string('order.html', {
            'products': products,
            'sell_number': Sells.get_order_number() + 1,
            'total': total
        })
        return HttpResponse(json.dumps({'order_html': order_html}), content_type='application/json')
    return HttpResponse(status=400)


def process_payment(request):
    if request.method == 'POST':
        order = json.loads(request.POST.get('order', '{}'))
        payment_type = request.POST.get('payment_type')
        order_number = Sells.get_order_number() + 1

        products_for_id = Product.objects.all()
        product_ids = [product.id for product in products_for_id]
        for product in order:
            if product != 'worker_id' and product != 'order_number' and int(product) in product_ids:
                product_db = get_object_or_404(Product, id=int(product))
                sell = Sells()
                sell.product = product_db.name
                sell.value_of_product = order[product]
                sell.worker = get_object_or_404(Worker, id=int(order['worker_id'])).name
                sell.order_number = order_number
                sell.payment_type = payment_type
                sell.save()
                product_db.value_on_warehouse -= order[product]
                product_db.save()

        success_html = render_to_string('success_payment.html')
        return HttpResponse(json.dumps({'success_html': success_html}), content_type='application/json')
    return HttpResponse(status=400)


def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        slug = request.POST.get('slug')
        category = Category()
        category.name = category_name
        category.slug = slug
        category.save()

    categories = Category.objects.all()
    return render(request, '../templates/show_categories.html', {'categories': categories})


def add_product(request):

    product_name = request.POST.get('product_name')
    slug = request.POST.get('slug')
    price = request.POST.get('price')
    category_slug = request.POST.get('category_slug')
    product = Product()
    product.name = product_name
    product.price = price
    product.category = get_object_or_404(Category, slug=category_slug)
    product.slug = slug
    product.status = True
    product.save()

    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, '../templates/products_by_category.html', {
        'category': category,
        'products': products,
        'slug': category_slug
    })


def pay(request):
    order_data = request.POST.get('order')
    order = json.loads(order_data)
    total = 0

    products_for_id = Product.objects.all()
    product_ids = [product.id for product in products_for_id]

    for product_id in order:
        if product_id != 'worker_id' and product_id != 'order_number' and int(product_id) in product_ids:
            product = get_object_or_404(Product, id=int(product_id))
            total += order[product_id] * int(product.price)

    return render(request, '../templates/pay.html', {
        'order': json.dumps(order),
        'total': total
    })