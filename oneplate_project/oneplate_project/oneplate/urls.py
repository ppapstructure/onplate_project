from django.urls import path

from oneplate.views import IndexView, UserProfileUpdateView, ReviewList

'''
profile-set과 profile-update가 같은 원리인데 이건 프론트한테 어떻게 하나 물어봐야겠다.
'''
'''
path('movies', MovieList.as_view()),
path('movies/<int:pk>', MovieDetail.as_view()),
'''


urlpatterns = [
    path('', IndexView.as_view(), name="index"),

    # Review
    path('reviews/', ReviewList.as_view(), name='review-list'),
    # auth
    path('auth/user/update/', UserProfileUpdateView.as_view(), name='profile-set'),

]