from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)

from blog.constants import POSTS_LIMIT
from blog.forms import CommentForm, PostForm, UserForm
from blog.mixins import CommentAccessMixin, PostMixin, PostAccessMixin
from blog.models import Category, Post
from blog.utils import get_post_qs


User = get_user_model()


class PostsListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = POSTS_LIMIT
    queryset = get_post_qs().annotate(comment_count=Count('comments'))


class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = POSTS_LIMIT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return context

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return category.posts.filter(
            is_published=True,
            pub_date__lt=timezone.now(),
        ).order_by('-pub_date').annotate(comment_count=Count('comments'))


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_object(self):
        post_obj = get_object_or_404(
            Post,
            pk=self.kwargs['post_id']
        )
        if post_obj.author != self.request.user:
            post_obj = get_object_or_404(
                Post,
                pk=self.kwargs['post_id'],
                is_published=True,
                category__is_published=True
            )
        return post_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class AuthorProfileView(ListView):
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    paginate_by = POSTS_LIMIT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username'],
        )
        return context

    def get_queryset(self):
        author = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        if author != self.request.user:
            return get_post_qs(
                author
            ).annotate(comment_count=Count('comments'))
        return Post.objects.select_related(
            'category',
            'location',
            'author'
        ).filter(
            author=author
        ).order_by('-pub_date').annotate(comment_count=Count('comments'))


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={
                'username': self.request.user
            }
        )


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={
                'username': self.request.user
            }
        )


class EditPostView(PostAccessMixin, LoginRequiredMixin, PostMixin, UpdateView):

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={
                'post_id': self.kwargs['post_id']
            }
        )


class EditCommentView(LoginRequiredMixin, CommentAccessMixin, UpdateView):
    form_class = CommentForm
    template_name = 'blog/create.html'


class DeletePostView(LoginRequiredMixin, PostAccessMixin,
                     PostMixin, DeleteView):
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())
        return context


class DeleteCommentView(LoginRequiredMixin, CommentAccessMixin, DeleteView):
    template_name = 'blog/comment.html'


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=pk)
