from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .models import Post
from .forms import PostEditForm
from django.contrib.auth.decorators import login_required

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

@login_required
def add_new_post(request):
    if request.method == 'POST':
        form = PostEditForm(request.POST)
        if form.is_valid():
            post = save_post_from_form(form, request.user)
            return redirect('post_details', pk=post.pk)
    else:
        form = PostEditForm()
        return render(request, 'blog/post_edit.html', {'form': form})

@login_required
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
    #post.published_date = timezone.now()
    post.save()
    return post

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_details', pk=pk)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

