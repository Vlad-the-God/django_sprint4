from django.utils import timezone

from blog.models import Post


def get_post_qs(author=None):
    posts = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        is_published=True,
        pub_date__lt=timezone.now(),
        category__is_published=True,
    ).order_by('-pub_date')
    if author is not None:
        return posts.filter(author=author)
    return posts
