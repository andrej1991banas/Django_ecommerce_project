from django import forms
from .models import Product
from .utils import generate_product_description



class AddProduct(forms.ModelForm):
        class Meta:
            model = Product
            fields = ['category', 'brand', 'model', 'price', 'image']


        def save(self, commit=True):

            product = super().save(commit=False)
            # product.category = self.cleaned_data['category'].capitalize()
            product.brand = self.cleaned_data['brand'].capitalize()
            product.model = self.cleaned_data['model'].capitalize()
            product.price = self.cleaned_data['price']
            product.image = self.cleaned_data.get('image')

            # Generate a description if not provided
            category_name=product.category.name
            prompt = f"Create a description for a {product.brand} {product.model} in the {category_name} category."
            product.description = generate_product_description(prompt) or "No description available."
            if commit:
                product.save()

            return product


class AddProductTest(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'brand', 'model', 'price', 'description']

    def save(self, commit=True):
        product = super().save(commit=False)
        product.category = self.cleaned_data['category'].capitalize()
        product.brand = self.cleaned_data['brand'].capitalize()
        product.model = self.cleaned_data['model'].capitalize()
        product.price = self.cleaned_data['price']
        product.description = self.cleaned_data('description')


        if commit:
            product.save()

        return product