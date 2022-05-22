import random
import string
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save


class Product(models.Model):
	title = models.CharField(max_length=30)
	slug = models.SlugField(blank=True, unique=True)
	description = models.TextField()
	price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99, null=True,)
	sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)

	def __str__(self):
		return self.title

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "{slug}-{rdstr}".format(slug=slug, rdstr=random_string_generator(size=4))
        return create_slug(instance, new_slug=new_slug)
    return slug


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
        
pre_save.connect(product_pre_save_receiver, sender=Product)

