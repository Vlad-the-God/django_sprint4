from django.urls import include, path

from . import views


app_name = 'blog'

posts_urls = [
    path(
        'create/',
        views.PostCreateView.as_view(), name='create_post'
    ),
    path(
        '<int:post_id>/',
        views.PostDetailView.as_view(), name='post_detail'
    ),
    path(
        '<int:post_id>/edit/',
        views.EditPostView.as_view(), name='edit_post'
    ),
    path(
        '<int:post_id>/delete/',
        views.DeletePostView.as_view(), name='delete_post'
    ),
    path(
        '<int:post_id>/edit_comment/<int:comment_id>/',
        views.EditCommentView.as_view(), name='edit_comment'
    ),
    path(
        '<int:post_id>/delete_comment/<int:comment_id>/',
        views.DeleteCommentView.as_view(), name='delete_comment'
    ),
]

urlpatterns = [
    path(
        '', views.PostsListView.as_view(), name='index'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostListView.as_view(), name='category_posts'
    ),
    path(
        'profile/<slug:username>/',
        views.AuthorProfileView.as_view(), name='profile'
    ),
    path(
        '<int:pk>/', views.add_comment, name='add_comment'
    ),
    path(
        'edit_profile/',
        views.EditProfileView.as_view(), name='edit_profile'
    ),
    path(
        'posts/', include(posts_urls)
    ),
]
