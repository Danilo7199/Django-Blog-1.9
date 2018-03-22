from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings   
# Create your views here.

from urllib.parse import quote_plus

from .forms import PostForm
from .models import post
from . import views
from django.contrib import messages
#Differ categories
def list_post(request, slug=None):
    qeryset_lsit = post.objects.all().order_by('-timestamp', '-updated')
    paginator = Paginator(qeryset_lsit, 8) # Show 8 contacts per page

    page = request.GET.get('page')
    try:
        qeryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        qeryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        qeryset = paginator.page(paginator.num_pages)

    context = {
        "post_list": qeryset,
        "title": "Post list"
    }
    return render(request, "index.html", context)
def create(request):
    if not request.user.is_staff or not request.is_superuser:
        settings.DEBUG=False
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        #success msg
        messages.success(request, "Posted", extra_tags='post_msg')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "form_post.html", context)


def update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        settings.DEBUG=False
        raise Http404
    instance = get_object_or_404(post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None ,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Edited", extra_tags='Edited _msg')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": "Edite list",
        "instance": instance,
        "form": form,
    }
    return render(request, "form_post.html", context)
    
def detail(request, slug=None):
    instance = get_object_or_404(post, slug=slug)
    share_string = quote_plus(instance.content)
    context = {
        "title": "Delete list",
        "instance": instance,
        "share_string": share_string, 
    }
    return render(request, "post_detail.html", context)
def delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        settings.DEBUG=False
        raise Http404
    instance = get_object_or_404(post, slug=slug)
    instance.delete()
    return redirect("list")
