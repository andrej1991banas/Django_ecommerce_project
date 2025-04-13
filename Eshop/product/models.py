from django.db import models
from djmoney.models.fields import MoneyField

class Category(models.Model):
    name = models.CharField(max_length=255)


    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    image = models.ImageField(upload_to='images/product/', blank=True, null=True)
    description = models.TextField()


    def __str__(self):
        return f'{self.brand} {self.model}'



    # def create_desc(self, prompt):
    #     """
    #     Creates a product description using an external AI API.
    #     """
    #     description = generate_product_description(prompt)
    #     if description:
    #         self.description = description
    #         self.save()

