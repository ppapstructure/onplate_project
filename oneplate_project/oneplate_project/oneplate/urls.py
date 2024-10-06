from django.urls import path

from oneplate.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
]