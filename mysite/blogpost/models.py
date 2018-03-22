from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils import timezone
from django.conf import settings

from django.utils.text import slugify

def upload_location(instance, filename):
    return "%s-%s" %(instance.id, filename)

class post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120) 
    slug = models.SlugField(unique=True, default=False)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,   auto_now_add=False)
        
    def __unicode__(self):
        return self.title
        
    def __str__(self):
        return self.title
    def get_absolute_url(self):#posts/id ______self.id
        return reverse("posts:detail", kwargs={"slug": self.slug}) #or
        #return "/posts/%s" %(self.id)

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

    pass

def pre_save_post_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)



pre_save.connect(pre_save_post_reciever, sender=post)
    
        
