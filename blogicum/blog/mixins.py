from django.shortcuts import redirect
from django.urls import reverse

from blog.models import Post
from blog.forms import PostForm


class PostMixin():
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'


class PostAccessMixin():

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect(
                'blog:post_detail',
                post_id=self.kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)


class CommentAccessMixin():

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return redirect(
                'blog:post_detail',
                post_id=self.kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={
                'post_id': self.kwargs['post_id']
            }
        )
