from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

    def clean_name(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        name = self.cleaned_data['name'].lower()
        for word in forbidden_words:
            if word in name:
                raise forms.ValidationError(f'Слово "{word}" запрещено в названии продукта.')
        return name

    def clean_description(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        description = self.cleaned_data['description'].lower()
        for word in forbidden_words:
            if word in description:
                raise forms.ValidationError(f'Слово "{word}" запрещено в описании продукта.')
        return description