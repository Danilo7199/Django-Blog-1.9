from django.contrib import admin
from .models import post

class ModelAdminSite(admin.ModelAdmin):
    list_display = ('__str__','title','updated', 'timestamp' )
    list_filter = ('updated', 'timestamp')
    list_editable= ('title',)

admin.site.register(post, ModelAdminSite)
# Register your models here.
