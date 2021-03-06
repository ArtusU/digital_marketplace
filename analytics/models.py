from django.conf import settings
from django.db import models

from tags.models import Tag


class TagViewManager(models.Manager):
    def add_count(self, user, tag):
        obj, created = self.model.objects.get_or_create(user=user, tag=tag)
        obj.count += 1
        obj.save()
        return obj
        
        

class TagView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    
    objects = TagViewManager()
    
    def __str__(self):
        return f"{self.tag.title}-{self.count}"