from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Contact, Version
from .forms import ProductForm
from django.shortcuts import render
from django.views import View


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()

        # Добавляем информацию об активной версии для каждого продукта
        for product in products:
            active_version = Version.objects.filter(product=product, is_active=True).first()
            product.active_version = active_version

        paginator = Paginator(products, 4)  # По 4 продуктов на страницу
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request, 'product_list.html', {'products': products})


class CreateProductView(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'create_product.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно создан.')
            return redirect('catalog:home')
        return render(request, 'create_product.html', {'form': form})


class EditProductView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        form = ProductForm(instance=product)
        return render(request, 'edit_product.html', {'form': form, 'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно отредактирован.')
            return redirect('catalog:product_detail', product_id=product_id)
        return render(request, 'edit_product.html', {'form': form, 'product': product})


class DeleteProductView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return render(request, 'delete_product.html', {'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        messages.success(request, 'Продукт успешно удален.')
        return redirect('catalog:product_list')


class HomeView(View):
    def get(self, request):
        latest_products = Product.objects.order_by('-created_at')[:5]
        return render(request, 'home.html', {'latest_products': latest_products})


class ContactsView(View):
    def get(self, request):
        contacts = Contact.objects.all()
        context = {'contacts': contacts}
        return render(request, 'contacts.html', context)


class SubmitFeedbackView(View):
    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact.objects.create(name=name, phone=phone, message=message)
        messages.success(request, 'Ваше сообщение успешно отправлено!')
        return redirect('catalog:contacts')


class ProductDetailView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return render(request, 'product_detail.html', {'product': product})
