import random
import os
import uuid
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# addional functions
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(instance.directory_string_var, filename)


def get_unique_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    instance_class = instance.__class__

    slug_exists = instance_class.objects.filter(slug=slug).exists()
    if slug_exists:
        new_slug = f'{slug}-{random.randint(0, 9)}'
        return get_unique_slug(instance, new_slug)
    else:
        return slug


# Models
class Category(models.Model):
    name = models.CharField(max_length=60, verbose_name="Nazwa kategorii")
    slug = models.SlugField(max_length=60, unique=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="Opis")

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:  # Create category
            self.slug = get_unique_slug(self)
        else:  # Update category
            if Category.objects.get(pk=self.pk).name != self.name:  # category name change so slug change
                self.slug = get_unique_slug(self)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tytuł")
    slug = models.SlugField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena")
    image = models.ImageField(upload_to=get_file_path, verbose_name="Zdjęcie")
    rate = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name="Opis")
    categories = models.ManyToManyField(Category, blank=True, verbose_name="Kategorie")

    directory_string_var = 'images'

    def get_rate_round_to_int(self):
        if self.rate is None:
            return 0
        else:
            return round(self.rate)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:  # Create Product
            self.slug = get_unique_slug(self)
        else:  # Update Product
            if Product.objects.get(pk=self.pk).name != self.name:  # Product name change so slug change
                self.slug = get_unique_slug(self)
        super(Product, self).save(*args, **kwargs)

    def save_without_new_slug(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

    def update_product_rating(self, comment_rate):
        comments_count = self.comment_set.count()
        if self.rate is None:
            new_rate = comment_rate
        else:
            new_rate = (comment_rate + comments_count*self.rate) / (comments_count + 1)
        print(f'New rate: {new_rate}')
        self.rate = new_rate
        self.save_without_new_slug()


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Twoja opinia")
    rating = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
