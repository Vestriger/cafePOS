from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cafe_management:products_by_category', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=1)
    status = models.BooleanField()
    value_on_warehouse = models.IntegerField(default=0)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def sliced(self):
        return self.name[:3]

    def get_absolute_url(self):
        return reverse('cafe_management:add_to_order', args=[self.id, self.slug])


class Worker(AbstractUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50, default="Barista")
    password = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.name


class Shifts(models.Model):
    time_start_shift = models.DateTimeField(auto_now_add=True)
    time_end_shift = models.DateTimeField(auto_now=True)
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True)
    opened = models.BooleanField(default=False)


class Sells(models.Model):
    product = models.CharField(max_length=100)
    worker = models.CharField(max_length=50)
    value_of_product = models.IntegerField(default=1)
    time_of_sell = models.DateField(auto_now_add=True)
    order_number = models.IntegerField(default=0)
    payment_type = models.CharField(max_length=50, default="none")

    @classmethod
    def get_order_number(cls):
        result = cls.objects.aggregate(models.Max('order_number'))
        return result['order_number__max'] or 1
