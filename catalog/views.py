from django.shortcuts import render, redirect


def home(request):
    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        # Обработка данных формы обратной связи
        pass
    return render(request, 'contacts.html')


def submit_feedback(request):
    if request.method == 'POST':
        # Обработка данных формы обратной связи
        # Здесь можно использовать Django Forms для более удобной обработки формы
        return redirect('catalog:contacts')
    else:
        # Вернуть что-то в случае GET-запроса (если это неожиданно)
        return redirect('catalog:contacts')
