from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def contacts(request):
    return render(request, 'contacts.html')


def submit_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        messages.success(request, 'Ваше сообщение успешно отправлено!')
        print(f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}')
        return redirect('catalog:contacts')
    else:
        return redirect('catalog:contacts')
