from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Contact, Version
from .forms import ProductForm, VersionForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views import View


class ProductListView(View):
    def get(self, request):
        # Упорядочиваем продукты по id перед пагинацией
        products = Product.objects.all().order_by('id')

        # Добавляем информацию об активной версии для каждого продукта
        for product in products:
            active_version = Version.objects.filter(product=product, is_active=True).first()
            product.active_version = active_version

        # Форма для добавления новой версии
        version_form = VersionForm()

        paginator = Paginator(products, 4)  # По 4 продукта на страницу
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request, 'product_list.html', {'products': products, 'version_form': version_form})


@method_decorator(login_required, name='dispatch')
class CreateProductView(View):
    template_name = 'create_product.html'

    def get(self, request):
        form = ProductForm()
        version_form = VersionForm()
        return render(request, self.template_name, {'form': form, 'version_form': version_form})

    @require_POST
    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        version_form = VersionForm(request.POST)

        if form.is_valid() and version_form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()

            version = version_form.save(commit=False)
            version.product = product
            version.save()

            return redirect('catalog:product_detail', product_id=product.id)

        return render(request, self.template_name, {'form': form, 'version_form': version_form})

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('users:login')  # Измените 'login' на ваш URL для страницы входа
        return super().dispatch(*args, **kwargs)


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
        product = Product.objects.get(pk=product_id)
        versions = Version.objects.filter(product=product)
        version_form = VersionForm()

        return render(request, 'product_detail.html', {'product': product, 'versions': versions, 'version_form': version_form})

    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        versions = Version.objects.filter(product=product)
        version_form = VersionForm(request.POST)

        if version_form.is_valid():
            version = version_form.save(commit=False)
            version.product = product
            version.save()
            return redirect('catalog:product_detail', product_id=product_id)

        return render(request, 'product_detail.html', {'product': product, 'versions': versions, 'version_form': version_form})


class AddVersionView(View):
    def post(self, request):
        version_form = VersionForm(request.POST)

        if version_form.is_valid():
            product_id = request.POST.get('product_id')  # Добавьте поле product_id в форму
            product = Product.objects.get(pk=product_id)

            # Деактивируем текущую активную версию продукта
            Version.objects.filter(product=product, is_active=True).update(is_active=False)

            # Создаем новую версию и делаем ее активной
            version = version_form.save(commit=False)
            version.product = product
            version.is_active = True
            version.save()

        return redirect('catalog:product_list')