from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .models import Post
from .forms import PostEditForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {
        'posts' : posts
    })

def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_details.html', {
        'post' : post
    })

def add_new_post(request):
    if request.method == 'POST':
        form = PostEditForm(request.POST)
        if form.is_valid():
            post = save_post_from_form(form, request.user)
            return redirect('post_details', pk=post.pk)
    else:
        form = PostEditForm()
        return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            post = save_post_from_form(form, request.user)
            return redirect('post_details', pk=post.pk)
    else:
        form = PostEditForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def save_post_from_form(form, user):
    post = form.save(commit=False)
    post.author = user
    post.published_date = timezone.now()
    post.save()
    return post


