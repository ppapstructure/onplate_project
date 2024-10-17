from django.urls import path,include
from rest_framework.routers import DefaultRouter
from oneplate.views import (
    IndexView,
    ReviewListView,
    ReviewCreateView,
    ReviewUpdateView,
    ReviewDeleteView,
    ReviewDetailView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    ProfileView,
    UserProfileSetView,
    UserProfileUpdateView,
    LikeViewSet,
    UserLikedReviewsView,
)

router = DefaultRouter()
router.register(r'likes', LikeViewSet, basename='like')

urlpatterns = [
    path('', IndexView.as_view(), name="index"),

    # Review
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/new/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/<int:review_id>/edit/', ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/<int:review_id>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('reviews/user/liked-reviews/', UserLikedReviewsView.as_view(), name='user-liked-reviews'),

    # Comment
    path(
        'reviews/<int:review_id>/comments/create/',
        CommentCreateView.as_view(),
        name='comment-create',
    ),
    path(
        'comments/<int:comment_id>/edit/',
        CommentUpdateView.as_view(),
        name='comment-update',
    ),
    path(
        'comments/<int:comment_id>/delete/',
        CommentDeleteView.as_view(),
        name='comment-delete',
    ),

    # profile
    path('users/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('set-profile/', UserProfileSetView.as_view(), name='profile-set'),
    path('edit-profile/', UserProfileUpdateView.as_view(), name='profile-update'),

    # like
    path('', include(router.urls)),
]
