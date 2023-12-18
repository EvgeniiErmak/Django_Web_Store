from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Contact


def home(request):
    # Добавляем выборку последних 5 товаров и выводим их в консоль
    latest_products = Product.objects.order_by('-created_at')[:5]
    for product in latest_products:
        print(f'ID: {product.id}, Name: {product.name}, Price: {product.price}')

    return render(request, 'home.html', {'latest_products': latest_products})


def contacts(request):
    # Получаем все контактные данные
    contacts = Contact.objects.all()

    # Остальной код для отображения страницы
    context = {'contacts': contacts}
    return render(request, 'contacts.html', context)


def submit_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Создаем объект Contact и сохраняем его в базу данных
        contact = Contact.objects.create(name=name, phone=phone, message=message)

        messages.success(request, 'Ваше сообщение успешно отправлено!')
        print(f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}')

        return redirect('catalog:contacts')
    else:
        return redirect('catalog:contacts')


def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'product_detail.html', {'product': product})
