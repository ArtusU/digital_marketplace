from django.contrib import admin
from products.models import Product, MyProducts, Thumbnail


class ThumbnailInline(admin.TabularInline):
	model = Thumbnail
	extra = 1
	
class ProductAdmin(admin.ModelAdmin):
	inlines = [ThumbnailInline]
	list_display = ["__str__", "description", "price", "sale_price"]
	search_fields = ["title", "description"]
	list_filter = ["price", "sale_price"]
	list_editable = ["sale_price"]
	class Meta:
		model = Product
  
admin.site.register(Product, ProductAdmin)
admin.site.register(MyProducts)
