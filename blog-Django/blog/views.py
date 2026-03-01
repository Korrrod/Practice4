from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegistrationForm, PostForm, CommentForm
from .models import Post, Tag, Follow, AccessRequest, Comment


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('feed')
    else:
        form = RegistrationForm()
    return render(request, 'blog/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('login')


def public_posts(request):
    posts = Post.objects.filter(visibility='public')
    return render(request, 'blog/public_posts.html', {'posts': posts})


@login_required
def feed(request):
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    all_posts = Post.objects.filter(author_id__in=following_ids) | Post.objects.filter(author=request.user)
    accessible_posts = [p for p in all_posts if p.can_view(request.user)]
    return render(request, 'blog/feed.html', {'posts': accessible_posts})


def _save_tags(post, tags_raw):
    names = [name.strip() for name in tags_raw.split(',') if name.strip()]
    tag_objs = []
    for name in names:
        tag, _ = Tag.objects.get_or_create(name=name)
        tag_objs.append(tag)
    post.tags.set(tag_objs)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            _save_tags(post, form.cleaned_data.get('tags', ''))
            messages.success(request, 'Пост опубликован.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            _save_tags(post, form.cleaned_data.get('tags', ''))
            messages.success(request, 'Пост обновлён.')
            return redirect('post_detail', pk=post.pk)
    else:
        initial_tags = ', '.join(post.tags.values_list('name', flat=True))
        form = PostForm(instance=post, initial={'tags': initial_tags})
    return render(request, 'blog/post_form.html', {'form': form, 'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.info(request, 'Пост удалён.')
        return redirect('feed')
    return render(request, 'blog/confirm_delete.html', {'post': post})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    can_view = post.can_view(request.user)
    access_requested = False
    pending_requests = []

    if request.user.is_authenticated and post.visibility == 'on_request':
        access_requested = AccessRequest.objects.filter(post=post, requester=request.user).exists()

    if request.user == post.author:
        pending_requests = post.access_requests.filter(status='pending')

    comment_form = CommentForm()
    if can_view and request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() and request.user.is_authenticated:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен.')
            return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'can_view': can_view,
        'comment_form': comment_form,
        'access_requested': access_requested,
        'pending_requests': pending_requests,
    })


@login_required
def request_access(request, pk):
    post = get_object_or_404(Post, pk=pk, visibility='on_request')
    if request.method != 'POST':
        return redirect('post_detail', pk=pk)
    if post.author == request.user:
        messages.info(request, 'Это ваш пост.')
        return redirect('post_detail', pk=pk)
    access_request, created = AccessRequest.objects.get_or_create(post=post, requester=request.user)
    if created:
        messages.success(request, 'Запрос отправлен автору.')
    else:
        messages.info(request, 'Запрос уже отправлен.')
    return redirect('post_detail', pk=pk)


@login_required
def handle_access_request(request, pk, action):
    access_request = get_object_or_404(AccessRequest, pk=pk, post__author=request.user)
    if request.method != 'POST':
        return redirect('post_detail', pk=access_request.post.pk)
    if action == 'approve':
        access_request.status = 'approved'
        messages.success(request, 'Доступ разрешён.')
    elif action == 'reject':
        access_request.status = 'rejected'
        messages.info(request, 'Запрос отклонён.')
    access_request.save()
    return redirect('post_detail', pk=access_request.post.pk)


@login_required
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        messages.info(request, 'Нельзя подписаться на себя.')
        return redirect('user_profile', username=username)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow.delete()
        messages.info(request, f'Вы отписались от {target.first_name or target.username}.')
    else:
        messages.success(request, f'Вы подписались на {target.first_name or target.username}.')
    return redirect('user_profile', username=target.username)


def user_profile(request, username):
    target_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=target_user)
    accessible_posts = [p for p in posts if p.can_view(request.user)]
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=target_user).exists()
    return render(request, 'blog/profile.html', {
        'target_user': target_user,
        'posts': accessible_posts,
        'is_following': is_following,
    })


@login_required
def my_blog(request):
    posts = Post.objects.filter(author=request.user)
    followers = Follow.objects.filter(following=request.user)
    return render(request, 'blog/my_blog.html', {'posts': posts, 'followers': followers})


def posts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    order = request.GET.get('order', 'new')
    posts = tag.posts.all()
    if order == 'old':
        posts = posts.order_by('id')
    accessible_posts = [p for p in posts if p.can_view(request.user)]
    return render(request, 'blog/tag_posts.html', {'tag': tag, 'posts': accessible_posts, 'order': order})
