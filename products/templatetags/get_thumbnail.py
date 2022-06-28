from codecs import register
from django import template

register = template.Library()

from ..models import Product, THUMB_CHOICES


@register.filter
def get_thumbnail(obj, arg):   
    arg = arg.lower()
    choices = dict(THUMB_CHOICES)
    
    if not isinstance(obj, Product):
        raise TypeError("This is not valid product model.")
    if not choices.get(arg):
        raise TypeError("This is not valid type of this model.") 
       
    return obj.thumbnail_set.filter(type=arg).first().media.url