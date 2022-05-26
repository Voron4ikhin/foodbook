from django.urls import path
from .views import post_comment_create_and_list_view, like_unlike_post, PostDeleteView, PostUpdateView, liked_posts_list_view, food_book_detail_view, PostDetailView

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_and_list_view, name='main-post-view'),
    path('myfoodbook/', liked_posts_list_view, name='liked_posts_view'),
    path('liked', like_unlike_post, name='like-post-view'),
    path('<pk>/', PostDetailView.as_view(), name='detail-post'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('foodbook/<slug>/', food_book_detail_view, name='liked_posts_user_profile'),
]