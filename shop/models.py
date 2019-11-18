import random
import os
import uuid
from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
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
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(self)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=get_file_path)
    rate = models.FloatField(default=0)
    description = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)

    directory_string_var = 'images'

    def get_rate_round_to_int(self):
        return round(self.rate)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(self)
        super(Product, self).save(*args, **kwargs)

    def save_without_new_slug(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

    def update_product_rating(self, comment_rate):
        comments_count = self.comment_set.count()
        new_rate = (comment_rate + comments_count*self.rate) / (comments_count + 1)
        self.rate = new_rate
        self.save_without_new_slug()


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name = "Twoja opinia")
    rating = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

