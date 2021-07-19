from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Store, CakeImage
from .forms import StoreForm

# Create your views here.

def home(request):
    #order_by -pub_date(최신순) pub_date(오래된순)
    posts = Store.objects.order_by('-pub_date')
    paginator = Paginator(posts, 2)
    page = request.GET.get('page', 1)
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'posts_list': posts})

def new(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            for img in request.FILES.getlist('imgs'):
                image = CakeImage()
                image.referred_store = post
                image.cake_image = img
                image.save()
            return redirect('home')
    else:
        form = StoreForm()

    return render(request, 'new.html', {'form': form})

def detail(request, pk):
    post = get_object_or_404(Store, pk=pk)
    return render(request, 'detail.html', {'post': post})

def edit(request, pk):
    post = get_object_or_404(Store, pk=pk)
    if request.method == "POST":
        form = StoreForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect('detail', pk= post.pk)
    else:
        form = StoreForm(instance=post)

    return render(request, 'edit.html', {'form': form})

def image_edit(request, pk):
    post = get_object_or_404(Store, pk=pk)
    if request.method == "POST":
        for img in request.FILES.getlist('imgs'):
            image = CakeImage()
            image.referred_store = post
            image.cake_image = img
            image.save()
        return redirect('detail', pk= post.pk)
    else:
        return render(request, 'image_edit.html',{'post':post})

def delete(request, pk):
    post = get_object_or_404(Store, pk=pk)
    post.delete()
    return redirect('home')

def image_delete(request, pk, image_pk):
    image = get_object_or_404(CakeImage, pk=image_pk)
    image.delete()
    return redirect('image_edit', pk=pk)