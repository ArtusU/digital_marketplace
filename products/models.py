from statistics import mode
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import random
import string
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save


def download_media_location(instance, filename):
	return "%s/%s" %(instance.slug, filename)


class Product(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_products", blank=True)
	media = models.FileField(blank=True, null=True, upload_to=download_media_location, storage=FileSystemStorage(location=settings.PROTECTED_ROOT))
	title = models.CharField(max_length=30)
	slug = models.SlugField(blank=True, unique=True)
	description = models.TextField()
	price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99, null=True,)
	sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("products:detail", kwargs={"slug": self.slug})

	def get_update_url(self):
		return reverse("products:update", kwargs={"slug": self.slug})

	def get_download(self):
		return reverse("products:download", kwargs={"slug": self.slug})
	

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


def thumbnail_location(instance, filename):
	return "%s/%s" %(instance.product.slug, filename)

class Thumbnail(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	height = models.CharField(max_length=20, null=True, blank=True )
	width = models.CharField(max_length=20, null=True, blank=True )
	media = models.ImageField(
		width_field = "width", 
  		height_field = "height", 
		blank=True, 
  		null=True, 
	 	upload_to=thumbnail_location
	   	)

	def __str__(self):
		return str(self.media.path)
	 

class MyProducts(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	products = models.ManyToManyField(Product, blank=True)
	
	
	def __str__(self):
		return "%s" %(self.products.count())
	
	class Meta:
		verbose_name = "My Products"
		verbose_name_plural = "My Products"

