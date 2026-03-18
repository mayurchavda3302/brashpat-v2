from django.shortcuts import render, get_object_or_404
from .models import Post, Tag


def post_list(request):
    """Blog listing — max 10 posts."""
    tag_slug = request.GET.get('tag')
    posts = Post.objects.filter(is_published=True).order_by('-published_at')
    active_tag = None
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)
    posts = posts[:10]  # Max 10 posts displayed
    tags = Tag.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts, 'tags': tags, 'active_tag': active_tag})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    recent_posts = Post.objects.filter(is_published=True).exclude(pk=post.pk).order_by('-published_at')[:4]
    return render(request, 'blog/post_detail.html', {'post': post, 'recent_posts': recent_posts})
