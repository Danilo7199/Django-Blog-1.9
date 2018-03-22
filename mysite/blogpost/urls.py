from django.conf.urls import url
from .views import(
	list_post,
	create,
	detail,
	update,
	delete,
	)

urlpatterns = [
    url(r'^$', list_post, name='list_post'),
    url(r'^create/$', create),
    url(r'^(?P<slug>[\w-]+)/$', detail, name="detail"),
    url(r'^(?P<slug>[\w-]+)/edit/$', update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', delete),
    
]
