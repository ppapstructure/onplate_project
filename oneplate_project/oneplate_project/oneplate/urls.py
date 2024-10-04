from django.urls import path
from oneplate.views import (
    IndexView,
    ReviewList,
    ReviewUpdateView,
    ReviewDeleteView,
    ReviewDetailView,
    ProfileView,
    UserProfileSetView,
    UserProfileUpdateView,
)

urlpatterns = [
    path('', IndexView.as_view(), name="index"),

    # Review
    path('reviews/', ReviewList.as_view(), name='review-list'),
    path('reviews/<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/<int:review_id>/edit/', ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/<int:review_id>/delete/', ReviewDeleteView.as_view(), name='review-delete'),

    # profile
    path('users/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('set-profile/', UserProfileSetView.as_view(), name='profile-set'),
    path('edit-profile/', UserProfileUpdateView.as_view(), name='profile-update'),
]